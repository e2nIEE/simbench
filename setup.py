# Copyright (c) 2019-2021 by University of Kassel, Tu Dortmund, RWTH Aachen University and Fraunhofer
# Institute for Energy Economics and Energy System Technology (IEE) Kassel and individual
# contributors (see AUTHORS file for details). All rights reserved.

from setuptools import setup, find_packages
import re

with open('README.rst', 'rb') as f:
    install = f.read().decode('utf-8')

with open('CHANGELOG.rst', 'rb') as f:
    changelog = f.read().decode('utf-8')

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
with open('.github/workflows/github_test_action.yml', 'rb') as f:
    lines = f.read().decode('utf-8')
    versions = set(re.findall('3.[0-9]', lines))
    for version in versions:
        classifiers.append('Programming Language :: Python :: 3.%s' % version[-1])

long_description = '\n\n'.join((install, changelog))

setup(
    name='simbench',
    version='1.3.0',
    author='Steffen Meinecke',
    author_email='steffen.meinecke@uni-kassel.de',
    description='Electrical Power System Benchmark Models',
    long_description=long_description,
    url='http://www.simbench.de/en',
    license='odbl',
    install_requires=["pandapower>=2.5"],
    extras_require={"docs": ["numpydoc", "sphinx", "sphinx_rtd_theme"],
                    "all": ["numpydoc", "sphinx", "sphinx_rtd_theme"]},
    packages=find_packages(),
    include_package_data=True,
    classifiers=classifiers
)
