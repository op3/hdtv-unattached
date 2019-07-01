#!/usr/bin/env python

from hdtv.version import __version__
from setuptools import setup
from distutils.command.build import build
import glob
import subprocess
import os

class CustomBuild(build):
    def run(self):
        # run original install code
        build.run(self)

        # Build libraries for this system
        # run hdtv --rebuild-sys after installation or any root version change
        # or reinstall from scratch
        for module in ['mfile-root', 'fit', 'display']:
            dir = os.path.join(self.build_lib, 'hdtv/rootext/', module)
            print("Building library in %s" % dir)
            subprocess.check_call(['make', '-j'], cwd=dir)

manpages = glob.glob('doc/guide/*.1')

KEYWORDS = '''\
analysis
data-analysis
gamma-spectroscopy
nuclear-physics
nuclear-spectrum-analysis
physics
python
root
root-cern
spectroscopy
'''
CLASSIFIERS = '''\
Development Status :: 5 - Production/Stable
Environment :: Console
Environment :: X11 Applications
Intended Audience :: Information Technology
Intended Audience :: Science/Research
License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
Natural Language :: English
Operating System :: MacOS
Operating System :: POSIX
Operating System :: POSIX :: Linux
Operating System :: UNIX
Programming Language :: C
Programming Language :: C++
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Information Analysis
Topic :: Scientific/Engineering :: Physics
Topic :: Scientific/Engineering :: Visualization
'''

setup(
    name='hdtv',
    version=version.__version__,
    description='HDTV - Nuclear Spectrum Analysis Tool',
    url='https://gitlab.ikp.uni-koeln.de/staging/hdtv',
    maintainer='Jan Mayer',
    maintainer_email='jan.mayer@ikp.uni-koeln.de',
    license='GPL',
    classifiers=CLASSIFIERS.strip().split('\n'),
    keywords=KEYWORDS.strip().replace('\n', ' '),
    install_requires=[
        'scipy',
        'matplotlib',
        'ipython'
        'prompt_toolkit',
        'traitlets',
        'uncertainties'],
    extras_require={
        'dev': ['docutils'],
        'test': ['pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'hdtv=hdtv.app:App',
        ]
    },
    packages=[
        'hdtv',
        'hdtv.backgroundmodels',
        'hdtv.plugins',
        'hdtv.peakmodels',
        'hdtv.efficiency',
        'hdtv.database',
        'hdtv.rootext',
    ],
    package_data={
        'hdtv': ['share/*'],
        'hdtv.rootext': [
            'Makefile', 'Makefile.def', 'Makefile.body',
            'mfile-root/*.hh', 'mfile-root/*.cc', 'mfile-root/Makefile',
            'mfile-root/LinkDef.h', 'mfile-root/libmfile-root.so',
            'mfile-root/libmfile-root_rdict.pcm',
            'mfile-root/libmfile-root.rootmap', 'mfile-root/matop/*.h',
            'mfile-root/matop/*.c',
            'fit/*.hh', 'fit/*.cc', 'fit/Makefile', 'fit/LinkDef.h',
            'fit/libfit.so', 'fit/libfit_rdict.pcm', 'fit/libfit.rootmap',
            'display/*.hh', 'display/*.cc', 'display/Makefile',
            'display/LinkDef.h', 'display/libdisplay.so',
            'display/libdisplay_rdict.pcm', 'display/libdisplay.rootmap',
            'util/Compat.hh'
        ],
    },
    data_files=[
        ('share/man/man1', manpages),
        ('share/zsh/site-functions', ['data/completions/_hdtv']),
        ('share/bash-completion/completions', ['data/completions/hdtv']),
        ('share/applications', ['data/hdtv.desktop']),
    ],
    cmdclass={
        'build': CustomBuild,
    }
)
