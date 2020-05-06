.. _installation:

===========================
Installation Guide
===========================

Installing Python
----------------------------

simbench is tested with Python 3.5, 3.6 and 3.7. We recommend the Anaconda Distribution, which provides a Python distribution that already includes a lot of modules for scientific computing that are needed. Of course it is also possible to use simbench with other distributions besides Anaconda. Anyway, it is important that the following package is included:

- pandapower



Installing simbench through pip
--------------------------------------------------------

The easiest way to install simbench is through pip:

1. Open a command prompt (e.g. start–>cmd on windows systems)

2. If you already work with the pandapower development version from GitHub, but did not yet register it to pip:

    a. Navigate your command prompt into your pandapower folder (with the command cd <folder>). 

    b. Register pandapower to pip, to not install pandapower a second time, via typing:

    :code:`pip install -e .`

3. Install simbench by running:

    :code:`pip install simbench`


Installing simbench without pip
--------------------------------------------------------

If you don't have internet access on your system or don't want to use pip for some other reason, simbench can also be installed without using pip:

1. Download and unzip the current simbench distribution from PyPi under "Download files".

2. Open a command prompt (e.g. Start-->cmd on Windows) and navigate to the folder that contains the setup.py file with the command cd <folder> :

    :code:`cd %path_to_simbench%\simbench-x.x.x\ `

3. Install simbench by running :

    :code:`python setup.py install`


Development Version
----------------------------

To install the latest version of simbench from github, simply follow these steps:

1. Download and install git.

2. Open a git shell and navigate to the directory where you want to keep your simbench files.

3. Run the following git command:

     :code:`git clone https://github.com/e2nIEE/simbench.git`

4. Open a command prompt (cmd or anaconda command prompt) and navigate to the folder where the simbench files are located. Run:

     :code:`pip install -e .`

     This registers your local simbench installation with pip.


Test your installation
----------------------------

A first basic way to test your installation is to import simbench to see if all dependencies are available:

import simbench

If you want to be really sure that everything works fine, run the simbench test suite:

1. Install pytest if it is not yet installed on your system:

    :code:`pip install pytest`

2. Run the simbench test suite:

     :code:`import simbench.test`

     :code:`simbench.test.run_all_tests()`

If everything is installed correctly, all tests should pass or xfail (expected to fail).
