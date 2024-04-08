# Copyright (c) 2019-2021 by University of Kassel, Tu Dortmund, RWTH Aachen University and Fraunhofer
# Institute for Energy Economics and Energy System Technology (IEE) Kassel and individual
# contributors (see AUTHORS file for details). All rights reserved.

import pytest

import simbench as sb

__author__ = "smeinecke"


def _occurance_test(code_list, code_to_test):
    assert code_to_test in code_list


def test_simbench_code_occurance():
    all_ = sb.collect_all_simbench_codes()

    _occurance_test(all_, "1-complete_data-mixed-all-1-sw")
    _occurance_test(all_, "1-EHVHVMVLV-mixed-all-2-sw")
    _occurance_test(all_, "1-HVMV-mixed-all-0-sw")
    _occurance_test(all_, "1-MVLV-urban-5.303-1-no_sw")
    _occurance_test(all_, "1-HV-mixed--0-sw")
    _occurance_test(all_, "1-MV-semiurb--0-sw")
    _occurance_test(all_, "1-LV-rural1--2-sw")
    _occurance_test(all_, "1-EHVHV-mixed-1-0-no_sw")
    _occurance_test(all_, "1-HV-urban--2-sw")


def test_simbench_code_conversion():
    all_ = sb.collect_all_simbench_codes()
    for input_code in all_:
        sb_code_parameters = sb.get_parameters_from_simbench_code(input_code)
        output_code = sb.get_simbench_code_from_parameters(sb_code_parameters)
        assert input_code == output_code


def test_collect_all_simbench_codes_on_a_sample_basis():

    all_codes = sb.collect_all_simbench_codes()
    assert len(all_codes) == 246
    _occurance_test(all_codes, '1-MVLV-rural-all-0-sw')

    single_zone_codes = sb.collect_all_simbench_codes(lv_level="", all_data=False)
    assert len(single_zone_codes) == 78
    _occurance_test(single_zone_codes, '1-MV-comm--1-no_sw')

    all_data_codes = sb.collect_all_simbench_codes(hv_level="")
    assert len(all_data_codes) == 6
    _occurance_test(all_data_codes, '1-complete_data-mixed-all-2-sw')

    mv_grids_without_switch_and_lv = sb.collect_all_simbench_codes(
            hv_level="MV", lv_level="", breaker_rep="no_sw", all_data=False)
    assert len(mv_grids_without_switch_and_lv) == 12
    _occurance_test(mv_grids_without_switch_and_lv, '1-MV-semiurb--1-no_sw')

    urban_hv_grid_scenario1_codes = sb.collect_all_simbench_codes(
            hv_level="HV", hv_type="urban", scenario=1, all_data=False)
    assert len(urban_hv_grid_scenario1_codes) == 10
    _occurance_test(urban_hv_grid_scenario1_codes, '1-HVMV-urban-4.201-1-no_sw')

    rural_and_urban_mv_grid_scenario1_codes = sb.collect_all_simbench_codes(
            hv_level="MV", lv_level="", hv_type=["rural", "urban"], scenario=1, all_data=False)
    assert len(rural_and_urban_mv_grid_scenario1_codes) == 4
    _occurance_test(rural_and_urban_mv_grid_scenario1_codes, '1-MV-rural--1-sw')


if __name__ == '__main__':
    if 0:
        pytest.main(["test_simbench_code.py", "-xs"])
    else:
        test_simbench_code_occurance()
        test_simbench_code_conversion()
        pass
