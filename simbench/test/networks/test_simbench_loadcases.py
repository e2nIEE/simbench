# Copyright (c) 2019-2021 by University of Kassel, Tu Dortmund, RWTH Aachen University and Fraunhofer
# Institute for Energy Economics and Energy System Technology (IEE) Kassel and individual
# contributors (see AUTHORS file for details). All rights reserved.

import pytest
import os

from simbench import sb_dir
import simbench.networks as sb

__author__ = "smeinecke"


def test_filter_loadcases():
    test_network_path = os.path.join(sb_dir, "test", "converter", "test_network")
    data = sb.read_csv_data(test_network_path, ";")
    assert data["StudyCases"].shape[0] == 24
    assert data["StudyCases"].shape[1]
    sb.filter_loadcases(data, factors=None)
    assert data["StudyCases"].shape[0] == 6


if __name__ == "__main__":
    if 0:
        pytest.main(["test_simbench_loadcases.py", "-xs"])
    else:
        test_filter_loadcases()
        pass
