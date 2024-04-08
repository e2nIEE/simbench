Change Log
=============

[1.5.1] - 2024-04-08
----------------------
[FIXED] spelling mistake in pyproject.toml

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
