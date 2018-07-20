# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, Caleb Bell <Caleb.Andrew.Bell@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

from __future__ import division
from ht import *
from scipy.constants import minute, hp
from ht.boiling_nucleic import _angles_Stephan_Abdelsalam
from numpy.testing import assert_allclose
import pytest

### Air Cooler

def test_air_cooler_Ft():    
    Ft_1 = Ft_aircooler(Thi=93, Tho=52, Tci=35, Tco=54.59, Ntp=2, rows=4)
    assert_allclose(Ft_1, 0.9570456123827129)
    
    # Example 2 as in [1]_; author rounds to obtain a slightly different result.
    Ft_2 = Ft_aircooler(Thi=125., Tho=45., Tci=25., Tco=95., Ntp=1, rows=4)
    assert_allclose(Ft_2, 0.5505093604092708)
    Ft_many = [[Ft_aircooler(Thi=125., Tho=80., Tci=25., Tco=95., Ntp=i, rows=j) for i in range(1,6)] for j in range(1, 6)]
    Ft_values = [[0.6349871996666123, 0.9392743008890244, 0.9392743008890244, 0.9392743008890244, 0.9392743008890244], [0.7993839562360742, 0.9184594715750571, 0.9392743008890244, 0.9392743008890244, 0.9392743008890244], [0.8201055328279105, 0.9392743008890244, 0.9784008071402877, 0.9392743008890244, 0.9392743008890244], [0.8276966706732202, 0.9392743008890244, 0.9392743008890244, 0.9828365967034366, 0.9392743008890244], [0.8276966706732202, 0.9392743008890244, 0.9392743008890244, 0.9392743008890244, 0.9828365967034366]]
    assert_allclose(Ft_many, Ft_values)
    
    
def test_air_cooler_noise_GPSA():
    noise = air_cooler_noise_GPSA(tip_speed=3177/minute, power=25.1*hp)
    assert_allclose(noise, 100.53680477959792)
    
    
def test_air_cooler_noise_Mukherjee():
    '''    # Confirmed to be log10's because of example tip speed reduction
    # of 60 m/s to 40 m/s saves 5.3 dB.
    # hp in shaft horse power
    # d in meters
    # sound pressure level, ref level 2E-5 pa

    '''
    noise = air_cooler_noise_Mukherjee(tip_speed=3177/minute, power=25.1*hp, fan_diameter=4.267)
    assert_allclose(noise, 99.11026329092925)
    
    noise = air_cooler_noise_Mukherjee(tip_speed=3177/minute, power=25.1*hp, fan_diameter=4.267, induced=True)
    assert_allclose(noise, 96.11026329092925)