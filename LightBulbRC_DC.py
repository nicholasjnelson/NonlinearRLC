#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 16:05:59 2023

@author: njnelson
"""

import numpy as np
import scipy.integrate as spi
import scipy.interpolate as spp
import matplotlib.pyplot as plt

def LB_rhs(t, Q, R_f):
    
    return -Q/(C*R_f())

data = np.loadtxt("LightbulbRC_Data_DC.csv", skiprows=2, delimiter=',')

time = data[:,0]
potential = data[:,1]
current = data[:,2]

resistance = potential/current

#R_func = spp.interp1d(current, resistance, kind='cubic')

