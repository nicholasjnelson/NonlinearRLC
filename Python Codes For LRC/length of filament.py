# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 11:31:08 2026

@author: AnthonySB2
"""
import numpy as np
r_L = 1.077e-5 / (2*np.pi)
print('r * L = ', r_L)

L = (r_L*50)**1/2
print('L=',L)

r = 1/50 * L
print('r=', r)
