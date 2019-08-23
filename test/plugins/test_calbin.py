"""
Artificial whether the calbin algorithm conserves the statistical properties of the spectrum by fitting a peak before and after calbinning.
"""

import os

from math import sqrt

import pytest
import xml.etree.ElementTree as ET

from test.helpers.utils import hdtvcmd, isclose
from test.helpers.create_test_spectrum import ArtificialSpec 
from test.helpers.fixtures import temp_file

from hdtv.util import monkey_patch_ui
monkey_patch_ui()

import hdtv.cmdline
import hdtv.options
import hdtv.session


import __main__
try:
    __main__.spectra = hdtv.session.Session()
except RuntimeError:
    pass

from hdtv.plugins.specInterface import spec_interface
from hdtv.plugins.fitInterface import fit_interface 
from hdtv.plugins.fitlist import fitxml

spectra = __main__.spectra

N_SIGMA = 3 # Determines how many standard deviations (sigma) a fitted quantity
# may deviate from the ideal value.
# Sigma is provided by the fitting algorithm .
UNCERTAINTY_RELATIVE_TOLERANCE = 0.2 # Determines how large the relative deviation, after calbinning, of the fit uncertainties from the original uncertainty may be.

# ts = 'test spectrum'
ts = ArtificialSpec()
ts.create()

def test_calbin(temp_file):
    command = ['spectrum get ' + ts.filename]

    step = 2 # Use the third spectrum which has a constant background and Poissonian fluctuations
    # Fit the peak in step 2
    command.append('fit marker background set %f' % ((step+ts.bg_regions[0][0])*ts.nbins_per_step))
    command.append('fit marker background set %f' % ((step+ts.bg_regions[0][1])*ts.nbins_per_step))
    command.append('fit marker background set %f' % ((step+ts.bg_regions[1][0])*ts.nbins_per_step))
    command.append('fit marker background set %f' % ((step+ts.bg_regions[1][1])*ts.nbins_per_step))

    command.append('fit marker region set %f' % ((step+0.5)*ts.nbins_per_step - 3.*ts.peak_width*ts.nbins_per_step))
    command.append('fit marker region set %f' % ((step+0.5)*ts.nbins_per_step + 3.*ts.peak_width*ts.nbins_per_step))
    command.append('fit marker peak set %f' % ((step+0.5)*ts.nbins_per_step))

    command.append('fit execute')
    command.append('fit store')
    f, ferr = hdtvcmd(*command)

    # Write the commands to a batch file
    batchfile = os.path.join(os.path.curdir, 'test', 'share', 'calbin.hdtv')
    with open(batchfile, 'w') as bfile:
        for c in command:
            bfile.write(c + '\n')

    assert ferr == ''

    # Write the fit result to a temporary XML file
    fitxml.WriteXML(spectra.Get("0").ID, temp_file)
    fitxml.ReadXML(spectra.Get("0").ID, temp_file, refit=True, interactive=False)

    # Parse XML file manually
    tree = ET.parse(temp_file)
    root = tree.getroot()

    # Check the number of fits
    fits = root.findall('fit')
    assert len(fits) == 1

    # Read out the main fitted peak properties (position, volume, width) and their uncertainties
    pos_value_init = float(fits[0].find('peak').find('cal').find('pos').find('value').text)
    pos_error_init = abs(float(fits[0].find('peak').find('cal').find('pos').find('error').text))
    vol_value_init = float(fits[0].find('peak').find('cal').find('vol').find('value').text)
    vol_error_init = abs(float(fits[0].find('peak').find('cal').find('vol').find('error').text))
    width_value_init = float(fits[0].find('peak').find('cal').find('width').find('value').text)
    width_error_init = abs(float(fits[0].find('peak').find('cal').find('width').find('error').text))

    # Calbin the spectrum with standard settings, read in the fitted value again and check whether they have changed
    command = ['spectrum calbin 0']
    command.append('fit execute')
    command.append('fit store')
    f, ferr = hdtvcmd(*command)
    assert ferr == ''

    # Write the commands to the same batch file
    batchfile = os.path.join(os.path.curdir, 'test', 'share', 'calbin.hdtv')
    with open(batchfile, 'a') as bfile:
        for c in command:
            bfile.write(c + '\n')

    assert ferr == ''

    fitxml.WriteXML(spectra.Get("0").ID, temp_file)
    fitxml.ReadXML(spectra.Get("0").ID, temp_file, refit=False, interactive=False)

    tree = ET.parse(temp_file)
    root = tree.getroot()

    fits = root.findall('fit')
    assert len(fits) == 3

    pos_value_1 = float(fits[2].find('peak').find('cal').find('pos').find('value').text)
    pos_error_1 = abs(float(fits[2].find('peak').find('cal').find('pos').find('error').text))
    vol_value_1 = float(fits[2].find('peak').find('cal').find('vol').find('value').text)
    vol_error_1 = abs(float(fits[2].find('peak').find('cal').find('vol').find('error').text))
    width_value_1 = float(fits[2].find('peak').find('cal').find('width').find('value').text)
    width_error_1 = abs(float(fits[2].find('peak').find('cal').find('width').find('error').text))

    assert isclose(pos_value_init - pos_value_1, 0., abs_tol=N_SIGMA*sqrt(pos_error_init*pos_error_init + pos_error_1*pos_error_1))
    assert isclose(vol_value_init - vol_value_1, 0., abs_tol=N_SIGMA*sqrt(vol_error_init*vol_error_init + vol_error_1*vol_error_1))
    assert isclose(width_value_init - width_value_1, 0., abs_tol=N_SIGMA*sqrt(width_error_init*width_error_init + width_error_1*width_error_1))

    # Calbin the spectrum with a factor of 2, read in the fitted value again and check whether they have changed
    command = ['spectrum calbin 0 -b 2']
    command.append('fit execute')
    command.append('fit store')
    f, ferr = hdtvcmd(*command)
    assert ferr == ''

    # Write the commands to the same batch file
    batchfile = os.path.join(os.path.curdir, 'test', 'share', 'calbin.hdtv')
    with open(batchfile, 'a') as bfile:
        for c in command:
            bfile.write(c + '\n')

    assert ferr == ''

    fitxml.WriteXML(spectra.Get("0").ID, temp_file)
    fitxml.ReadXML(spectra.Get("0").ID, temp_file, refit=False, interactive=False)

    tree = ET.parse(temp_file)
    root = tree.getroot()

    fits = root.findall('fit')
    assert len(fits) == 7

    pos_value_2 = float(fits[6].find('peak').find('cal').find('pos').find('value').text)
    pos_error_2 = abs(float(fits[6].find('peak').find('cal').find('pos').find('error').text))
    vol_value_2 = float(fits[6].find('peak').find('cal').find('vol').find('value').text)
    vol_error_2 = abs(float(fits[6].find('peak').find('cal').find('vol').find('error').text))
    width_value_2 = float(fits[6].find('peak').find('cal').find('width').find('value').text)
    width_error_2 = abs(float(fits[6].find('peak').find('cal').find('width').find('error').text))

    assert isclose(pos_value_init - pos_value_2, 0., abs_tol=N_SIGMA*sqrt(pos_error_init*pos_error_init + pos_error_2*pos_error_2))
    assert isclose(vol_value_init - vol_value_2, 0., abs_tol=N_SIGMA*sqrt(vol_error_init*vol_error_init + vol_error_2*vol_error_2))
    assert isclose(width_value_init - width_value_2, 0., abs_tol=N_SIGMA*sqrt(width_error_init*width_error_init + width_error_2*width_error_2))
    
    assert isclose(pos_error_init, pos_error_2, rel_tol=0.2)
    assert isclose(vol_error_init, vol_error_2, rel_tol=0.2)
    assert isclose(pos_error_init, pos_error_2, rel_tol=0.2)