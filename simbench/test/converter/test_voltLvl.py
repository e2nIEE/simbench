# Copyright (c) 2019-2021 by University of Kassel, Tu Dortmund, RWTH Aachen University and Fraunhofer
# Institute for Energy Economics and Energy System Technology (IEE) Kassel and individual
# contributors (see AUTHORS file for details). All rights reserved.

import pytest
from numpy import array
import pandapower as pp
import pandapower.networks as pn

import simbench as sb

__author__ = "smeinecke"


def test_convert_voltlvl_names():
    voltlvl_names = sb.convert_voltlvl_names([1, 2, "hv", 4, 5, "ehv", 7], str)
    assert voltlvl_names == ["EHV", "EHV-HV", "HV", "HV-MV", "MV", "EHV", "LV"]
    voltlvl_names = sb.convert_voltlvl_names([1, 2, "hv", 4, 5, "ehv", 7], int)
    assert voltlvl_names == [1, 2, 3, 4, 5, 1, 7]


def test_voltlvl_idx():
    net = pn.example_multivoltage()
    # add measurements
    pp.create_measurement(net, "v", "bus", 1.03, 0.3, net.bus.index[7])  # 380 kV
    pp.create_measurement(net, "v", "bus", 1.03, 0.3, net.bus.index[40])  # 10 kV
    pp.create_measurement(net, "i", "trafo", 0.23, 0.03, net.trafo.index[-1], "hv")  # 10 kV
    pp.create_measurement(net, "p", "trafo", 0.33, 0.03, net.trafo.index[0], "lv")  # 110 kV
    pp.create_measurement(net, "i", "line", 0.23, 0.03, net.line.index[-1], "to")  # 0.4 kV
    pp.create_measurement(net, "q", "line", 0.33, 0.03, net.line.index[0], "from")  # 110 kV

    # checking voltlvl_idx()
    hv_and_mv_buses = list(range(16, 45))
    assert hv_and_mv_buses == sb.voltlvl_idx(net, "bus", 4)
    assert hv_and_mv_buses == sb.voltlvl_idx(net, "bus", ["HV-MV"])
    assert hv_and_mv_buses == sb.voltlvl_idx(net, "bus", [3, 5])
    assert hv_and_mv_buses == sb.voltlvl_idx(net, "bus", ["HV", "MV"])
    mv_loads = list(range(5, 13))
    assert mv_loads == sb.voltlvl_idx(net, "load", "MV")
    hvmv_trafo3ws = [0]
    assert hvmv_trafo3ws == sb.voltlvl_idx(net, "trafo3w", "HV", branch_bus="hv_bus")
    assert hvmv_trafo3ws == sb.voltlvl_idx(net, "trafo3w", "MV", branch_bus="mv_bus")
    assert hvmv_trafo3ws == sb.voltlvl_idx(net, "trafo3w", "MV", branch_bus="lv_bus")
    ehvhv_trafos = [0]
    assert ehvhv_trafos == sb.voltlvl_idx(net, "trafo", 1, branch_bus="hv_bus")
    assert ehvhv_trafos == sb.voltlvl_idx(net, "trafo", 3, branch_bus="lv_bus")
    ehvhv_and_hvmv_trafos = [0]
    assert ehvhv_and_hvmv_trafos == sb.voltlvl_idx(net, "trafo", 2, branch_bus="hv_bus")
    assert ehvhv_and_hvmv_trafos == sb.voltlvl_idx(net, "trafo", 4, branch_bus="lv_bus")
    hvmv_trafos = []
    assert hvmv_trafos == sb.voltlvl_idx(net, "trafo", 5, branch_bus="lv_bus")
    mvlv_trafos = [1]
    assert mvlv_trafos == sb.voltlvl_idx(net, "trafo", 5, branch_bus="hv_bus")
    lv_loads = list(range(13, 25))
    assert lv_loads == sb.voltlvl_idx(net, "load", 7)
    m1 = sb.voltlvl_idx(net, "measurement", [1])
    m3 = sb.voltlvl_idx(net, "measurement", 3)
    m5 = sb.voltlvl_idx(net, "measurement", 5)
    m7 = sb.voltlvl_idx(net, "measurement", 7)
    assert m1 == [0]
    assert m3 == [3, 5]
    assert m5 == [1, 2]
    assert m7 == [4]
    assert len(net.measurement.index) == len(m1+m3+m5+m7)
    assert set(net.measurement.index) == set(m1) | set(m3) | set(m5) | set(m7)


def test_all_voltlvl_idx():
    net = pn.example_simple()

    lvl_dicts = sb.all_voltlvl_idx(net)

    elms = set()
    for elm in pp.pp_elements():
        if net[elm].shape[0]:
            elms |= {elm}
            idxs = set()
            for _, idx in lvl_dicts[elm].items():
                idxs |= idx
            assert set(net[elm].index) == idxs
    assert elms == set(lvl_dicts.keys())

    elms = ["bus"]
    lvl_dicts = sb.all_voltlvl_idx(net, elms=elms)
    assert list(lvl_dicts.keys()) == elms

    lvl_dicts = sb.all_voltlvl_idx(net, elms=["bus", "trafo3w"], include_empty_elms_dicts=True)
    assert not bool(net.trafo3w.shape[0])
    assert "trafo3w" in lvl_dicts.keys()


def test_get_voltlvl():
    input1 = [146, 145, 144, 61, 60, 59, 2, 1, 0.8]
    input2 = 0.4
    assert all(sb.get_voltlvl(input1) == array([1, 3, 3, 3, 5, 5, 5, 7, 7]))
    assert sb.get_voltlvl(input2) == 7


if __name__ == "__main__":
    if 0:
        pytest.main(["test_voltLvl.py", "-xs"])
    else:
        # test_convert_voltlvl_names()
        # test_voltlvl_idx()
        # test_get_voltlvl()
        test_all_voltlvl_idx()
        pass
