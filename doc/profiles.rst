#############################
SimBench Profiles
#############################


Within the dataset SimBench provides a large number of full year load, generation and storage profiles.

The profiles are already included in the pandapower nets received by the function:

.. code:: python

    net = simbench.get_simbench_net(sb_code_info)
    net.profiles

If you are not interested in the SimBench grids, you can get the profiles easily using this function:

.. autofunction:: simbench.get_all_simbench_profiles

Several other functions are provided for advanced use, such as:

.. autofunction:: simbench.get_applied_profiles

.. autofunction:: simbench.get_available_profiles

.. autofunction:: simbench.get_missing_profiles

.. autofunction:: simbench.profiles_are_missing

.. autofunction:: simbench.get_absolute_profiles_from_relative_profiles

.. autofunction:: simbench.get_absolute_values

.. autofunction:: simbench.apply_const_controllers
