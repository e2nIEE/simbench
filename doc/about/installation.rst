.. _installation:

===========================
Installation Guide
===========================

Installing Python
----------------------------

simbench is tested with multiple up-to-date Python versions. We recommend the Miniconda Distribution, which provides a Python distribution that already includes a lot of modules for scientific computing that are needed. Of course it is also possible to use simbench with other distributions besides Anaconda. Anyway, it is important that the following package is included:

- pandapower



Installing simbench through pip
--------------------------------------------------------

The easiest way to install simbench is through pip:

1. Open a command prompt (e.g. start–>cmd on windows systems)

2. Install simbench by running:

    :code:`pip install simbench`


Installing simbench without internet connection
--------------------------------------------------------

If you don't have internet access on your system and already downloaded the repository (step 1), simbench can also be installed without from local files:

1. Download and unzip the current simbench distribution from PyPi under "Download files".

2. Open a command prompt (e.g. Start-->cmd on Windows) and navigate to the folder that contains the setup.py file with the command cd <folder> :

    :code:`cd %path_to_simbench%\simbench-x.x.x\ `

3. Install simbench by running :

    :code:`pip install -e .`

     This registers your local pandapower installation with pip, the option -e ensures the edits in the files have a direct impact on the pandapower installation.


Development Version
----------------------------

To install the latest version of simbench from github, simply follow these steps:

1. Download and install git.

2. Open a git shell and navigate to the directory where you want to keep your simbench files.

3. Run the following git command:

     :code:`git clone https://github.com/e2nIEE/simbench.git`

4. Open a command prompt (cmd or anaconda command prompt) and navigate to the folder where the simbench files are located. Run:

     :code:`pip install -e .`

     This registers your local pandapower installation with pip, the option -e ensures the edits in the files have a direct impact on the pandapower installation.


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
