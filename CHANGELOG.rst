Change Log
=============

[1.6.1] - 2024-04-13
----------------------
- [CHANGED] nothing - just a correct upload to pypi

[1.6.0] - 2024-04-09
----------------------
- [CHANGED] support pandapower geojson, released with pandapower version 3.0.0
- [ADDED] support pandapower parameters step_dependency_table and tap_dependency_table, released with pandapower version 3.0.0
- [CHANGED] drop python 3.8 support
- [FIXED] fix ValueError raise according to GitHub issue #56
- [CHANGED] rename parameter csv2pp parameter `no_generic_coord` by `fill_bus_geo_by_generic_data`

[1.5.3] - 2024-04-23
----------------------
- [FIXED] Bringing together develop and master with all changes of the release process
- [ADDED] generalization and test for auxiliary function :code:`to_numeric_ignored_errors()`

[1.5.2] - 2024-04-09
----------------------
- [CHANGED] readded copyright notice to setup.py and updated date
- [CHANGED] added prune to MANIFEST.in to exclude doc and tutorials from wheel builds
- [CHANGED] removed gitlab ci files from MANIFEST.in to keep them out of wheel builds
- [CHANGED] updated pyproject.toml to fix build issues
- [CHANGED] updated upload_release.yml to not call setup.py anymore (see https://packaging.python.org/en/latest/discussions/setup-py-deprecated/)
- [CHANGED] updated upload_release.yml to build and upload src dist as .tar.gz and .whl
- [CHANGED] updated upload_release.yml to install from PyPI and test the installed package

[1.5.1] - 2024-04-08
----------------------
- [FIXED] spelling mistake in pyproject.toml

[1.5.0] - 2024-04-08
----------------------
- [CHANGED] apply FutureWarnings of pandas 2.2
- [CHANGED] increase visibility of collect_all_simbench_codes()
- [CHANGED] setup.py -> pyproject.toml

[1.4.0] - 2023-05-12
----------------------
- [CHANGED] pandas 2.0 support
- [CHANGED] pandapower 2.12.1 support
- [ADDED] GitHub Actions Workflow (:code:`release.yml`) to automate the SimBench release process

[1.3.0] - 2021-11-25
----------------------

- [CHANGED] use GitHub-Ci instead of Travis-CI and update CI to python 3.8 and 3.9
- [CHANGED] adapt to pandas changes of version 1.2.0: deprecate set operations for pandas Index
- [CHANGED] generalize (elm, col) recognizing in profiles dicts
- [CHANGED] output type of get_applied_profiles() and get_available_profiles() from list to set
- [ADDED] filter_unapplied_profiles_pp(), get_unused_profiles()

[1.2.0] - 2020-09-29
----------------------

- [CHANGED] Storage profiles with curtailment and self-consumption; ChargeLevel and EStore of storages
- [FIXED] PowerPlantProfiles: add missing hour at time change
- [FIXED] adapt to pandapower changes: import unsupplied_buses()

[1.1.0] - 2020-05-07
----------------------

- [FIXED] bug in "element2" column of measurement tables of the scenario 1 and 2 data at HV and MV connections
- [FIXED] commercial MV grid connection to HV1 bug
- [CHANGED] Storage.csv column names correction: max_e_mwh -> eStore, efficency_percent -> etaStore, self-discharge_percent_per_day -> sdStore
- [REMOVED] converter: remove obsolete parameter resistance_ohm
- [FIXED] auxiliary nodes with multiple branches connected are removed
- [FIXED] generate_no_sw_variant(): replace auxiliary type of buses with no switch connected

[1.0.0] - 2019-05-15
----------------------

- [ADDED] python code to utilize the SimBench dataset with pandapower
- [ADDED] complete grids, profiles and study cases dataset of SimBench project
