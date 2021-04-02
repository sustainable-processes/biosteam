# -*- coding: utf-8 -*-
# BioSTEAM: The Biorefinery Simulation and Techno-Economic Analysis Modules
# Copyright (C) 2020-2021, Yoel Cortes-Pena <yoelcortes@gmail.com>
# 
# This module is under the UIUC open-source license. See 
# github.com/BioSTEAMDevelopmentGroup/biosteam/blob/master/LICENSE.txt
# for license details.
"""
"""
from .decorators import cost
from ..utils.unit_warnings import lb_warning
from .._unit import Unit

__all__ = ('ScrewFeeder',)

@cost('Flow rate', lb=400, ub=10e4, CE=567, cost=1096, n=0.22)
class ScrewFeeder(Unit):
    length = 30 #: ft
    _N_outs = 1
    _has_power_utility = True
    _units = {'Flow rate': 'ft^3/hr'}
    
    def _design(self):
        feed = self.ins[0]
        self.design_results['Flow rate'] = feed.F_vol * 35.315 # ft3/hr
        F_mass = 0.0006124 * feed.F_mass # lb/s
        self.power_utility.consumption = 0.0146 * F_mass**0.85 * self.length * 0.7457