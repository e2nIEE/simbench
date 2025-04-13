# Copyright (c) 2019-2021 by University of Kassel, Tu Dortmund, RWTH Aachen University and Fraunhofer
# Institute for Energy Economics and Energy System Technology (IEE) Kassel and individual
# contributors (see AUTHORS file for details). All rights reserved.

import pytest
import os
from copy import deepcopy
from packaging import version
import numpy as np
import pandas as pd
import pandapower as pp
from pandapower.networks import example_simple

from simbench import sb_dir
from simbench.converter import csv2pp, csv_data2pp, pp2csv, pp2csv_data, \
    convert_parallel_branches, read_csv_data, ensure_full_column_data_existence, \
    avoid_duplicates_in_column, merge_busbar_coordinates, to_numeric_ignored_errors, \
    repl_nans_in_obj_cols_to_empty_str

try:
    import pandaplan.core.pplog as logging
except ImportError:
    import logging

logger = logging.getLogger(__name__)

simbench_converter_test_path = os.path.join(sb_dir, "test", "converter")
test_network_path = os.path.join(simbench_converter_test_path, "test_network")
test_output_folder_path = os.path.join(simbench_converter_test_path, "test_network_output_folder")

__author__ = 'smeinecke'


def test_convert_to_parallel_branches():
    # create test grid
    net = pp.create_empty_network()
    pp.create_bus(net, 110)
    pp.create_buses(net, 2, 20)

    # --- transformers & corresponding switches
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="Trafo 1")
    pp.create_switch(net, 1, 0, "t", name="Tr-Switch 1")
    # only name changed:
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="Trafo 2")
    pp.create_switch(net, 1, 1, "t", name="Tr-Switch 2")
    # only max_loading changed:
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="Trafo 1", max_loading_percent=50)
    pp.create_switch(net, 1, 2, "t", name="Tr-Switch 1")
    # only switch position changed:
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="Trafo 1")
    pp.create_switch(net, 1, 3, "t", closed=False, name="Tr-Switch 1")
    # only switch missing:
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="Trafo 1")
    # only name and std_type changed:
    pp.create_transformer(net, 0, 1, "25 MVA 110/20 kV", name="Trafo 3")
    pp.create_switch(net, 1, 5, "t", name="Tr-Switch 3")
    # only name changed and switch added:
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="Trafo 4")
    pp.create_switch(net, 1, 6, "t", name="Tr-Switch 4a")
    pp.create_switch(net, 0, 6, "t", name="Tr-Switch 4b")
    # only name and parallel changed:
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="Trafo 5", parallel=2)
    pp.create_switch(net, 1, 7, "t", name="Tr-Switch 5")

    # --- lines & corresponding switches
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="Line 1")
    pp.create_switch(net, 2, 0, "l", name="L-Switch 1")
    # only name changed:
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="Line 2")
    pp.create_switch(net, 2, 1, "l", name="L-Switch 2")
    # only max_loading changed:
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="Line 1", max_loading_percent=50)
    pp.create_switch(net, 2, 2, "l", name="L-Switch 1")
    # only switch position changed:
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="Line 1")
    pp.create_switch(net, 2, 3, "l", closed=False, name="L-Switch 1")
    # only switch missing:
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="Line 1")
    # only name and std_type changed:
    pp.create_line(net, 1, 2, 1.11, "48-AL1/8-ST1A 20.0", name="Line 3")
    pp.create_switch(net, 2, 5, "l", name="L-Switch 3")
    # only name changed and switch added:
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="Line 4")
    pp.create_switch(net, 2, 6, "l", name="L-Switch 4a")
    pp.create_switch(net, 1, 6, "l", name="L-Switch 4b")
    # only name and parallel changed:
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="Line 5", parallel=2)
    pp.create_switch(net, 2, 7, "l", name="L-Switch 5")
    # only name and from_bus <-> to_bus changed:
    pp.create_line(net, 2, 1, 1.11, "94-AL1/15-ST1A 20.0", name="Line 6")
    pp.create_switch(net, 2, 8, "l", name="L-Switch 6")

    net1 = deepcopy(net)
    net2 = deepcopy(net)
    net3 = deepcopy(net)

    # complete
    convert_parallel_branches(net1, multiple_entries=False)
    for elm in ["trafo", "line"]:
        assert sorted(net1[elm].index) == [0, 2, 3, 4, 5, 6]
    assert list(net1["trafo"].parallel.values) == [4] + [1]*5
    assert list(net1["line"].parallel.values) == [5] + [1]*5

    # only line
    convert_parallel_branches(net2, multiple_entries=False, elm_to_convert=["line"])
    assert pp.dataframes_equal(net2.line, net1.line)
    assert pp.dataframes_equal(net2.trafo, net.trafo)

    # only exclude "max_loading_percent"
    convert_parallel_branches(net3, multiple_entries=False, exclude_cols_from_parallel_finding=[
                                      "name", "parallel", "max_loading_percent"])
    for elm in ["trafo", "line"]:
        assert sorted(net3[elm].index) == [0, 3, 4, 5, 6]
    assert list(net3["trafo"].parallel.values) == [5] + [1]*4
    assert list(net3["line"].parallel.values) == [6] + [1]*4


def test_convert_parallel_branches():
    # create test grid
    net = pp.create_empty_network()
    pp.create_bus(net, 110)
    pp.create_buses(net, 4, 20)
    pp.create_ext_grid(net, 0)
    pp.create_load(net, 4, 1e3, 4e2)
    pp.create_transformer(net, 0, 1, "40 MVA 110/20 kV", name="sd", parallel=3)
    pp.create_switch(net, 1, 0, "t", name="dfjk")
    pp.create_line(net, 1, 2, 1.11, "94-AL1/15-ST1A 20.0", name="sdh", parallel=2)
    pp.create_switch(net, 2, 0, "l", name="dfsdf")
    pp.create_line(net, 2, 3, 1.11, "94-AL1/15-ST1A 20.0", name="swed", parallel=1)
    pp.create_line(net, 3, 4, 1.11, "94-AL1/15-ST1A 20.0", name="sdhj", parallel=3)
    pp.create_switch(net, 3, 2, "l", name="dfdfg")
    pp.create_switch(net, 4, 2, "l", False, name="dfhgj")
    # check test grid
    assert net.trafo.shape[0] == 1
    assert net.line.shape[0] == 3
    assert net.switch.shape[0] == 4

    convert_parallel_branches(net)
    # test parallelisation
    assert net.trafo.shape[0] == 3
    assert net.line.shape[0] == 6
    assert net.switch.shape[0] == 11

    net1 = deepcopy(net)
    net1.switch.loc[4, "closed"] = False
    convert_parallel_branches(net, multiple_entries=False)
    convert_parallel_branches(net1, multiple_entries=False)
    # test sum up of parallels
    assert net.trafo.shape[0] == 1
    assert net.line.shape[0] == 3
    assert net.switch.shape[0] == 4
    assert net1.trafo.shape[0] == 1
    assert net1.line.shape[0] == 4
    assert net1.switch.shape[0] == 5


def test_test_network():
    net = csv2pp(test_network_path, fill_bus_geo_by_generic_data=False)

    # test min/max ratio
    for elm in pp.pp_elements(bus=False, branch_elements=False, other_elements=False):
        if "min_p_mw" in net[elm].columns and "max_p_mw" in net[elm].columns:
            isnull = net[elm][["min_p_mw", "max_p_mw"]].isnull().any(axis=1)
            assert (net[elm].min_p_mw[~isnull] <= net[elm].max_p_mw[~isnull]).all()
        if "min_q_mvar" in net[elm].columns and "max_q_mvar" in net[elm].columns:
            isnull = net[elm][["min_q_mvar", "max_q_mvar"]].isnull().any(axis=1)
            assert (net[elm].min_q_mvar[~isnull] <= net[elm].max_q_mvar[~isnull]).all()

    pp2csv(net, test_output_folder_path, export_pp_std_types=False, drop_inactive_elements=False)

    # --- test equality of exported csv data and given csv data
    csv_orig = read_csv_data(test_network_path, ";")
    csv_exported = read_csv_data(test_output_folder_path, ";")

    all_eq = True
    for tablename in csv_orig.keys():
        try:
            params = {"tol": 1e-7} if version.parse(pp.__version__) <= version.parse("2.7.0") else \
                dict()
            eq = pp.dataframes_equal(csv_orig[tablename], csv_exported[tablename], **params)
            if not eq:
                logger.error("csv_orig['%s'] and csv_exported['%s'] differ." % (tablename,
                                                                                tablename))
                logger.error(csv_orig[tablename].head())
                logger.error(csv_exported[tablename].head())
                logger.error(csv_orig[tablename].dtypes)
                logger.error(csv_exported[tablename].dtypes)
        except ValueError:
            eq = False
            logger.error("dataframes_equal did not work for %s." % tablename)
        all_eq &= eq
    assert all_eq


def test_example_simple():
    net = example_simple()

    # --- fix scaling
    net.load["scaling"] = 1.

    # --- add some additional data
    net.bus["subnet"] = ["net%i" % i for i in net.bus.index]
    pp.create_measurement(net, "i", "trafo", np.nan, np.nan, 0, "hv", name="1")
    pp.create_measurement(net, "i", "line", np.nan, np.nan, 1, "to", name="2")
    pp.create_measurement(net, "v", "bus", np.nan, np.nan, 0, name="3")

    net.shunt["max_step"] = np.nan
    stor = pp.create_storage(net, 6, 0.01, 0.1, -0.002, 0.05, 80, name="sda", min_p_mw=-0.01,
                             max_p_mw=0.008, min_q_mvar=-0.01, max_q_mvar=0.005)
    net.storage.loc[stor, "efficiency_percent"] = 90
    net.storage.loc[stor, "self-discharge_percent_per_day"] = 0.3
    pp.create_dcline(net, 4, 6, 0.01, 0.1, 1e-3, 1.0, 1.01, name="df", min_q_from_mvar=-0.01)
    pp.runpp(net)
    to_drop = pp.create_bus(net, 7, "to_drop")

    # --- add names to elements
    for i in pp.pp_elements():
        net[i] = ensure_full_column_data_existence(net, i, 'name')
        avoid_duplicates_in_column(net, i, 'name')

    # --- create geodata
    net.bus["geo"] = list(map(lambda xy: f'{{"type":"Point", "coordinates":[{xy[0]}, {xy[1]}]}}',
                              zip([0., 1., 2., 3., 4., 5., 5., 3.63], [0.]*5+[-5., 5., 2.33])))
    merge_busbar_coordinates(net, False)

    # --- convert
    csv_data = pp2csv_data(net, export_pp_std_types=True, drop_inactive_elements=True)
    net_from_csv_data = csv_data2pp(csv_data)

    # --- adjust net appearance / define what should be compared
    pp_is_27lower = version.parse(pp.__version__) <= version.parse("2.7.0")

    pp.drop_buses(net, [to_drop])
    if "power_station_trafo" in net.gen.columns:
        assert net.gen["power_station_trafo"].isnull().all()
        del net.gen["power_station_trafo"]
    net.load["type"] = np.nan

    # compare std_types as dataframes
    for netx in [net, net_from_csv_data]:
        for key, vals in netx["std_types"].items():
            netx[f"std_types|{key}"] = to_numeric_ignored_errors(pd.DataFrame(vals).T)

    for key in net.keys():
        if isinstance(net[key], pd.DataFrame):
            # drop unequal columns
            dummy_columns = net[key].columns
            extra_columns = net_from_csv_data[key].columns.difference(dummy_columns)
            net_from_csv_data[key] = net_from_csv_data[key].drop(columns=extra_columns)
            # adjust dtypes
            if net[key].shape[0]:
                try:
                    net_from_csv_data[key] = net_from_csv_data[key].astype(dtype=dict(net[
                        key].dtypes))
                except:
                    logger.error("dtype adjustment of %s failed." % key)
            # drop result table rows
            if pp_is_27lower and "res_" in key:
                if key != "res_bus":
                    net[key] = net[key].iloc[0:0]
                else:
                    net[key].loc[:, ["p_mw", "q_mvar"]] = np.nan

    repl_nans_in_obj_cols_to_empty_str(net)
    repl_nans_in_obj_cols_to_empty_str(net_from_csv_data)

    # --- for pp2.7.1 and newer
    if not pp_is_27lower:
        name_selection = [key for key in net.keys() if key.startswith("std_types|")]
        for elm in sorted(pp.pp_elements()):
            if net[elm].shape[0] == net_from_csv_data[elm].shape[0] == 0:
                assert not len(net[elm].columns.symmetric_difference(
                    net_from_csv_data[elm].columns))
            else:
                name_selection.append(elm)
        eq = pp.nets_equal(net, net_from_csv_data, name_selection=name_selection,
                           check_without_results=True)

    # --- for older pp versions
    else:
        net_from_csv_data.converged = net.converged
        del net["OPF_converged"]
        del net_from_csv_data["substation"]
        del net_from_csv_data["profiles"]
        del net["std_types"]
        del net_from_csv_data["std_types"]

        eq = pp.nets_equal(net, net_from_csv_data, tol=1e-7)
    assert eq


if __name__ == "__main__":
    if 0:
        pytest.main([__file__, "-xs"])
    else:
        test_convert_to_parallel_branches()
        test_convert_parallel_branches()
        test_test_network()
        test_example_simple()
        pass
