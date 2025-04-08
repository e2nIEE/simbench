# Copyright (c) 2019-2021 by University of Kassel, Tu Dortmund, RWTH Aachen University and Fraunhofer
# Institute for Energy Economics and Energy System Technology (IEE) Kassel and individual
# contributors (see AUTHORS file for details). All rights reserved.

import numpy as np
import pandas as pd
from collections import OrderedDict
from pandapower.timeseries import DFData
from pandapower.control import ConstControl

from simbench import csv_tablenames, idx_in_2nd_array, merge_dataframes

try:
    import pandaplan.core.pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)

__author__ = 'smeinecke'


def get_applied_profiles(net, profile_type):
    """ Returns a list of unique profiles in element tables, e.g. net.sgen.profile.
        profile_type must be in ["load", "renewables", "powerplants", "storage"]. """
    applied_profiles = set()
    if profile_type in ["renewables", "powerplants"]:
        phys_type = "RES" if profile_type == "renewables" else "PowerPlant"
        fitting_elm = {"renewables": "sgen", "powerplants": "gen"}[profile_type]
        for elm in ['sgen', 'gen', 'ext_grid']:
            if 'profile' in net[elm].columns:
                if "phys_type" in net[elm].columns:
                    idx = net[elm].index[net[elm].phys_type == phys_type]
                else:
                    idx = net[elm].index if elm == fitting_elm else []
                applied_profiles |= set(net[elm].profile[idx].dropna())
    else:
        if 'profile' in net[profile_type].columns:
            applied_profiles |= set(net[profile_type].profile.dropna())
    return applied_profiles


def get_available_profiles(net, profile_type, p_or_q=None, continue_on_missing=False):
    """ Returns a list of unique profiles in net.profiles.
        profile_type in ["load", "renewables", "powerplants", "storage"]
        p_or_q can be None, "p", or "q" """
    p_or_q = None if profile_type != "load" else p_or_q
    if "profiles" in net.keys() and profile_type in net["profiles"].keys():
        avail_prof = net["profiles"][profile_type].columns
        avail_prof = avail_prof if "time" not in avail_prof else avail_prof.difference(["time"])
        avail_prof = pd.Series(avail_prof)
        if p_or_q is None:
            return set(avail_prof)
        elif p_or_q == "p":
            return set(avail_prof.loc[avail_prof.str.endswith("_pload")].str[:-6])
        elif p_or_q == "q":
            return set(avail_prof.loc[avail_prof.str.endswith("_qload")].str[:-6])
        else:
            raise ValueError(str(p_or_q) + " is unknown as 'p_or_q'.")
    elif continue_on_missing:
        logger.warning("%s is not in net['profiles'].keys()" % profile_type)
        return set()
    else:
        raise ValueError("%s is not in net['profiles'].keys()" % profile_type)


def get_missing_profiles(net, profile_type, p_or_q=None):
    """ Returns a set of profiles which miss in net.profiles compared to the profile column of the
        element table. """
    return get_applied_profiles(net, profile_type) - get_available_profiles(
        net, profile_type, p_or_q=p_or_q)


def get_unused_profiles(net, profile_type, p_or_q=None):
    """ Returns a set of profiles which is in net.profiles but is not used in the profile column
        of the element table. """
    if profile_type == "load" and p_or_q is None:
        applied_ = set()
        for s in get_applied_profiles(net, profile_type):
            applied_ |= {"%s_pload" % s, "%s_qload" % s}
        availp = {"%s_pload" % s for s in get_available_profiles(net, profile_type, "p")}
        availq = {"%s_qload" % s for s in get_available_profiles(net, profile_type, "q")}
        return (availp | availq) - applied_
    else:
        return get_available_profiles(net, profile_type, p_or_q=p_or_q) - \
            get_applied_profiles(net, profile_type)


def dismantle_dict_values_to_deep_list(dict_):
    """ returns a list of dict values even if the values of the dict are dicts again. """
    dict_ = OrderedDict(sorted(dict_.items()))
    return [val if not isinstance(val, dict) else dismantle_dict_values_to_deep_list(
            val) for val in dict_.values()]


def dismantle_dict_values_to_list(dict_):
    """ returns a list of dict values even if the values of the dict are dicts again. """
    dict_ = OrderedDict(sorted(dict_.items()))
    list_ = []
    for val in dict_.values():
        if not isinstance(val, dict):
            list_.append(val)
        else:
            list_ += dismantle_dict_values_to_list(val)
    return list_


def profiles_are_missing(net, return_as_bool=True):
    """ Checks whether any of the used profiles (requested in net[elm].profile) misses in
        net.profiles. """
    profile_types = ["load", "renewables", "powerplants", "storage"]
    return_ = dict.fromkeys(profile_types)
    return_["load"] = {"p": "p", "q": "q"}

    for profile_type in return_.keys():
        if isinstance(return_[profile_type], dict):
            for p_or_q in return_[profile_type].keys():
                return_[profile_type][p_or_q] = get_missing_profiles(net, profile_type,
                                                                     p_or_q=p_or_q)
        else:
            return_[profile_type] = get_missing_profiles(net, profile_type)
    if return_as_bool:
        return bool(len(set.union(*dismantle_dict_values_to_list(return_)).difference(
                set([np.nan]))))
    else:
        return return_


def filter_unapplied_profiles(csv_data):
    """ Filters unapplied profiles from csv_data. """
    profile_tables = csv_tablenames('profiles')
    element_tables = list(pd.Series(profile_tables).str.split("Profile", expand=True)[0])
    for prof_tab, elm_tab in zip(profile_tables, element_tables):
        applied_profiles = list(csv_data[elm_tab].profile.dropna().unique())
        if elm_tab == "Load" and len(applied_profiles):
            applied_profiles_p = pd.Series(applied_profiles) + "_pload"
            applied_profiles_q = pd.Series(applied_profiles) + "_qload"
            applied_profiles = list(applied_profiles_p) + list(applied_profiles_q)
        applied_profiles.append("time")
        unapplied_profiles = csv_data[prof_tab].columns.difference(applied_profiles)
        logger.debug("These %ss are dropped: " % prof_tab + str(unapplied_profiles))
        csv_data[prof_tab] = csv_data[prof_tab].drop(unapplied_profiles, axis=1)


def filter_unapplied_profiles_pp(net, named_profiles: bool):
    """ Filters unapplied profiles from pandapower net. """
    if "profiles" in net and isinstance(net["profiles"], dict):
        if named_profiles:
            for key in net["profiles"].keys():
                unused = get_unused_profiles(net, key)
                net.profiles[key] = net.profiles[key].drop(columns=unused)
        else:
            for key in net.profiles.keys():
                if isinstance(key, tuple):
                    elm = key[0]
                elif isinstance(key, str):
                    elm = key.split(".")[0]
                else:
                    raise NotImplementedError("The keys of net.profiles are expected as " +
                                              "tuple(element, column) or as str, e.g. 'gen.vm_pu'.")
                net.profiles[key] = net.profiles[key].drop(columns=net.profiles[key].columns[
                    ~net.profiles[key].columns.isin(net[elm].index)])


def get_absolute_profiles_from_relative_profiles(
        net, element, multiplying_column, relative_profiles=None, profile_column="profile",
        profile_suffix=None, time_as_index=False, **kwargs):
    """
    Returns a DataFrame with profiles for the given element (e.g. loads or sgens). The profiles
    values are calculated by multiplying the relative profiles given by relative_profiles
    (or if not given, from net["profiles"]) with the values in net[element][multiplying_column].

    INPUT:
        **net** (pandapowerNet) - pandapower net

        **element** (str) - element type for which absolute profiles are calculated. Possible are
        "load", "gen", "sgen" or "storage".

        **multiplying_column** (str) - column name within net[element].columns which should be
        multiplied with the relative profiles. Usual multiply_columns are 'p_mw' or 'q_mvar'.
        Additional Feature: If multiplying_column is not a string, the relative profiles are not
        multiplied with net[element][multiplying_column] but with 'multiplying_column' itself.

    OPTIONAL:
        **relative_profiles** (DataFrame, None) - DataFrame of relative profiles as input. If None,
        net["profiles"] is considered.

        **profile_column** (str, "profile") - Name of the column which contains information about
        which element is assigned to which profile. In SimBench grids, this information is
        given in the column "profile". For that reason, 'profile' is the default.

        **profile_suffix** (str, None) - For the case that different profiles are given for p and q,
        these can be distinguished by a suffix. For loads this can be "_pload" and "_qload",
        which will be automatically assumed, if profile_suffix is None.

        **time_as_index** (bool, False) - If True, the returned DataFrame has
        relative_profiles["time"] as index. If False, relative_profiles.index is used.

        ****kwargs** - key word arguments for merge_dataframes()

    OUTPUT:
        **output_profiles** (DataFrame) - calculated absolute profiles
    """
    # --- use net.profiles if relative_profiles is None
    if relative_profiles is None:
        if element in ["load", "storage"]:
            relative_profiles = net.profiles[element]
        elif element in ["gen", "sgen"]:
            # Since RES and Powerplants can be converted to pandapower as both, gen or sgen, both
            # are considered together
            relative_profiles = merge_dataframes(
                [net.profiles["powerplants"], net.profiles["renewables"]], **kwargs)
        else:
            raise ValueError("element %s is unknown." % str(element))

    # --- set index
    index = relative_profiles["time"] if time_as_index else relative_profiles.index

    # --- do profile_suffix assumptions if profile_suffix is None
    if profile_suffix is None:
        profile_suffix = ""
        if element == "load":
            if multiplying_column == "p_mw":
                profile_suffix = "_pload"
            elif multiplying_column == "q_mvar":
                profile_suffix = "_qload"

    # --- get relative profiles
    relative_profiles_vals = np.ones((len(index), len(net[element])))
    if profile_column in net[element].columns:
        applied_profiles = net[element][profile_column] + profile_suffix

        missing = list(applied_profiles[~applied_profiles.isin(relative_profiles.columns)])
        if len(missing):
            raise ValueError("These profiles are set to be applied but are missing in the profiles "
                             "data: " + str(missing))
        isna = applied_profiles.isnull()
        is_not_na_pos = np.arange(len(isna), dtype=int)[~isna.values]
        relative_profiles_vals[:, is_not_na_pos] = \
            relative_profiles[list(applied_profiles[~isna])].values

    else:  # warning and assumptions in case of missing profile column
        logger.warning("In %s table, profile column '%s' is missing. Scalings of 1 are assumed." % (
            element, profile_column))

    # --- get factor to multiply with (consider additional feature of 'multiplying_column')
    if isinstance(multiplying_column, str):
        if multiplying_column in net[element].columns:
            factor = net[element][multiplying_column].values.reshape(1, -1)
        else:
            raise ValueError("'multiplying_column' %s is not in net[%s].columns." % (
                multiplying_column, element))
    else:
        factor = multiplying_column

    # --- multiply relative profiles with factor and return results
    output_profiles = pd.DataFrame(relative_profiles_vals*factor, index=index,
                                   columns=net[element].index)
    return output_profiles


def get_absolute_values(net, profiles_instead_of_study_cases, **kwargs):
    """
    Is a convenience function using get_absolute_profiles_from_relative_profiles(). This function
    returns a dict with all absolute values, calculated from scaling factors and maximum
    active or reactive powers.

    INPUT:
        **net** (pandapowerNet) - pandapower net

        **profiles_instead_of_study_cases** (bool) - Flag to decide whether profiles or loadcases
        should be considered.

        ****kwargs** - key word arguments for get_absolute_profiles_from_relative_profiles()
        (especially for merge_dataframes())

    OUTPUT:
        **abs_val** (dict) - absolute values calculated from relative scaling factors and maximum
        active or reactive powers. The keys of this dict are tuples consisting of element and
        column or of strings consisting of the same but splitted by '.'.
        The values are DataFrames with absolute power values.
    """
    abs_val = dict()

    if profiles_instead_of_study_cases:  # use given profiles
        for elm_col in [("load", "p_mw"), ("load", "q_mvar"), ("sgen", "p_mw"), ("gen", "p_mw"),
                        ("storage", "p_mw")]:
            abs_val[elm_col] = get_absolute_profiles_from_relative_profiles(
                net, elm_col[0], elm_col[1], **kwargs)

    else:  # use predefined study cases

        # --- voltage set point
        slack_base_case = pd.DataFrame(net["ext_grid"]["vm_pu"].values.reshape(1, -1),
                                       columns=net["ext_grid"].index, index=["bc"])
        abs_val[("ext_grid", "vm_pu")] = pd.DataFrame(net.loadcases["Slack_vm"].values.reshape(
            -1, 1).repeat(net["ext_grid"].shape[0], axis=1), columns=net["ext_grid"].index,
            index=net.loadcases["Slack_vm"].index)
        abs_val[("ext_grid", "vm_pu")] = pd.concat([slack_base_case,
                                                   abs_val[("ext_grid", "vm_pu")]])

        # --- active and reactive scaling factors
        for elm_col in [("load", "p_mw"), ("load", "q_mvar"), ("sgen", "p_mw")]:

            loadcase_type = {"load": {"p_mw": "pload",
                                      "q_mvar": "qload"},
                             "sgen": {"p_mw": ["Wind_p", "PV_p", "RES_p"]}}[elm_col[0]][elm_col[1]]
            if isinstance(loadcase_type, list):
                assert elm_col[0] == "sgen"
                assert len(loadcase_type) == 3
                Idx_wind = net.sgen.index[(net.sgen.type.str.contains("Wind").fillna(False)) |
                                        (net.sgen.type.str.contains("WP").fillna(False))]
                Idx_pv = net.sgen.index[net.sgen.type.str.contains("PV").fillna(False)]
                Idx_sgen = net.sgen.index.difference(Idx_wind.union(Idx_pv))
                net.sgen["loadcase_type"] = ""
                net.sgen.loc[Idx_wind, 'loadcase_type'] = loadcase_type[0]
                net.sgen.loc[Idx_pv, 'loadcase_type'] = loadcase_type[1]
                net.sgen.loc[Idx_sgen, 'loadcase_type'] = loadcase_type[2]
            else:
                net[elm_col[0]]["loadcase_type"] = loadcase_type

            abs_val[elm_col] = get_absolute_profiles_from_relative_profiles(
                net, elm_col[0], elm_col[1], profile_column="loadcase_type",
                relative_profiles=net.loadcases, profile_suffix="", **kwargs)
            base_case = pd.DataFrame(net[elm_col[0]][elm_col[1]].values.reshape(1, -1),
                                     columns=net[elm_col[0]].index, index=["bc"])
            abs_val[elm_col] = pd.concat([base_case, abs_val[elm_col]])

            del net[elm_col[0]]["loadcase_type"]

    return abs_val


def apply_const_controllers(net, absolute_profiles_values, exclude_elms_dict=None):
    """
    Applys ConstControl instances to the net. As a result, one can easily run timeseries with given
    power values of e.g. loads, sgens, storages or gens.

    INPUT:
        **net** - pandapower net

        **absolute_profiles_values** - dict of Dataframes with absolute values for the profiles,
        keys should be tuples of length 2 (element and parameter), DataFrame size is
        timesteps x number of elements

    OPTIONAL:
        **exclude_elms_dict** (dict, None) - elements which should not get ConstControllers. The
        keys should be the element type, such as "sgen", and the values should be the indices.
    """
    n_time_steps = dict()
    for key, values in absolute_profiles_values.items():
        if isinstance(key, tuple):
            elm = key[0]
            col = key[1]
        elif isinstance(key, str):
            elm = key.split(".")[0]
            col = key.split(".")[1]
        else:
            raise NotImplementedError("The keys of net.profiles are expected as " +
                                      "tuple(element, column) or as str, e.g. 'gen.vm_pu'.")
        if values.shape[1]:
            to_exclude = pd.Index([]) if not isinstance(exclude_elms_dict, dict) or elm not in \
                exclude_elms_dict.keys() else pd.Index(exclude_elms_dict[elm])

            # check DataFrame shape[0] == time_steps
            if elm in n_time_steps.keys():
                if n_time_steps[elm] != values.shape[0]:
                    logger.warning("There are two profiles for %ss which have different " % elm +
                                   "amount of time steps.")
            else:
                n_time_steps[elm] = values.shape[0]

            # check DataFrame shape[1] == net[elm].index
            unknown_idx = values.columns.difference(net[elm].index)
            if len(unknown_idx):
                logger.warning("In absolute_profiles_values[%s], " % key +
                               "there are indices additional & unknown to net[%s].index" % elm +
                               str(["%i" % i for i in unknown_idx]))
            missing_idx = net[elm].index.difference(values.columns.union(to_exclude))
            if len(missing_idx):
                logger.warning("In absolute_profiles_values[%s], " % key +
                               "these indices are missing compared to net[%s].index" % elm +
                               str(["%i" % i for i in missing_idx]))

            # apply const controllers
            idx = list(net[elm].index.difference(to_exclude).intersection(values.columns))
            ConstControl(net, element=elm, variable=col,
                         element_index=idx, profile_name=idx,
                         data_source=DFData(absolute_profiles_values[key][idx]))

    # compare all DataFrame shape[0] == time_steps
    if len(set(n_time_steps.values())) > 1:
        logger.warning("The profiles have different amount of time steps:")
        logger.warning(n_time_steps)


if __name__ == "__main__":
    pass
