
.. image:: https://simbench.de/wp-content/uploads/2019/01/logo.png
   :target: https://www.simbench.net
   :alt: SimBench logo

.. image:: https://badge.fury.io/py/simbench.svg
   :target: https://pypi.python.org/pypi/simbench
   :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/simbench.svg
   :target: https://pypi.python.org/pypi/simbench
   :alt: versions

.. image:: https://readthedocs.org/projects/simbench/badge/?version=stable
   :target: http://simbench.readthedocs.io/?badge=stable
   :alt: Documentation Status

.. image:: https://github.com/e2nIEE/simbench/actions/workflows/github_test_action.yml/badge.svg
   :target: https://github.com/e2nIEE/simbench/actions/
   :alt: GitHub Actions

.. image:: https://codecov.io/github/e2nIEE/simbench/coverage.svg?branch=master
   :target: https://app.codecov.io/github/e2nIEE/simbench?branch=master
   :alt: codecov

.. image:: https://pepy.tech/badge/simbench
   :target: https://pepy.tech/project/simbench
   :alt: pepy

.. image:: https://img.shields.io/badge/License-ODbL-brightgreen.svg
   :target: https://opendatacommons.org/licenses/odbl
   :alt: ODbL

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://github.com/e2nIEE/simbench/blob/master/LICENSE
   :alt: BSD

SimBench (www.simbench.net) is a research project to create a "simulation database for uniform comparison of innovative solutions in the field of network analysis, network planning and operation", which was conducted for three and a half years from 1.11.2015 to 30.04.2019. It was part of the German Federal Government's 6th Energy Research Program "Research for an Environmentally Friendly, Reliable and Affordable Energy Supply". The project was carried out by the University of Kassel, the Fraunhofer IEE, the RWTH Aachen University and the Technical University of Dortmund in accordance with the authors mentioned above. The project, coordinated by the University of Kassel, was supported by the professional advisory from six German distribution network operators: DREWAG NETZ GmbH, Energie Netz Mitte GmbH, ENSO NETZ GmbH, Netze BW GmbH, Syna GmbH and Westnetz GmbH.

The objective of the research project SimBench is the development of a benchmark dataset to support research in grid planning and operation. SimBench grids differ from existing grids in the following key aspects:

- Consideration of a wide range of use cases during the development of datasets
- Provision of grid data for low voltage (LV), medium voltage (MV), high voltage (HV), extra-high voltage (EHV) as well as design of data for a suitable interconnection of a grid among different voltage levels for cross-level simulations
- Ensuring high reproducibility and comparability by providing clearly assigned load and generation time series
- Validation of the suitability of the datasets with simulation, deliberately determined grid states including suitable dimensioning of grid assets

This repository provides data and code to use SimBench within the software pandapower (www.pandapower.org).
