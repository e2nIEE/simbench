# Copyright (c) 2015-2019 by University of Kassel and Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.

from setuptools import setup, find_packages
import re

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3']
with open('.travis.yml', 'rb') as f:
    lines = f.read().decode('utf-8')
    for version in re.findall('python: 3.[0-9]', lines):
        classifiers.append('Programming Language :: Python :: 3.%s'%version[-1])

setup(
    name='simbench',
    version='1.1.0',
    author='Steffen Meinecke',
    author_email='steffen.meinecke@uni-kassel.de',
    description='Electrical Power System Benchmark Models',
    long_description=readme,
    url='http://www.simbench.de/en',
    license='odbl',
    install_requires=["pandapower>=2.2"],
    extras_require = {"docs": ["numpydoc", "sphinx", "sphinx_rtd_theme"]},
    packages=find_packages(),
    include_package_data=True,
    classifiers = classifiers
)
