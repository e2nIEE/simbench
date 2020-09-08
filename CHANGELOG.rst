Change Log
=============

[develop]
----------------------

- [CHANGED] Storage profiles with curtailment and self-consumption; ChargeLevel and EStore of storages
- [FIXED] PowerPlantProfiles: add missing hour at time change

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
