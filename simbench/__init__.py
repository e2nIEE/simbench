# Copyright (c) 2019-2021 by University of Kassel, Tu Dortmund, RWTH Aachen University and Fraunhofer
# Institute for Energy Economics and Energy System Technology (IEE) Kassel and individual
# contributors (see AUTHORS file for details). All rights reserved.

import importlib.metadata
import os

__author__ = "smeinecke"
__version__ = importlib.metadata.version("simbench")
sb_dir = os.path.dirname(os.path.realpath(__file__))

from simbench.converter import *
from simbench.networks import *
