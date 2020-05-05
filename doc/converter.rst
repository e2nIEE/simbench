#############################
Converter
#############################

.. |br| raw:: html

    <br />

.. _Converter:

Besides the grid, profiles and study cases data, this repository provides the converter between pandapower net format and csv files with SimBench data format.

.. autofunction:: simbench.csv2pp

.. autofunction:: simbench.pp2csv

|br|

The converter functions use internal functions which converts between a pandapower net object and a dict object with SimBench data format.
This internal functions can be used if no writing or reading from and to csv files is desired.

|br|

.. autofunction:: simbench.csv_data2pp

.. autofunction:: simbench.pp2csv_data
