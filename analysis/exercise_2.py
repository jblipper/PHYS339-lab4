# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:06:49 2023

@author: Bhuvan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rcParams.update({'font.size': 22})

I1 = np.array([0,300,600,900,1200,1500,1800,2100,2400,2700,3000,3900,4095])
I2 = np.array([i for i in range(0,2500,100)])
I3 = np.array([i for i in range(0,2500,100)])

R = 100
errR = 10

V1 = np.array([0.002,0.369,0.737,1.109,1.470,1.656,1.657,1.657,1.657,1.657,1.657,1.657,1.657])
V2 = np.array([0.002,0.129,0.247,0.369,0.493,0.616,0.737,0.857,0.982,1.109,1.232,1.349,1.471,1.596, 1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660])
V3 = np.array([0.003,0.129,0.246,0.369,0.493,0.617,0.737,0.857,0.982,1.109,1.232,1.349,1.471,1.596, 1.661,1.662,1.662,1.662,1.662,1.662,1.662,1.662,1.662,1.662,1.662])
V = (V2+V3)/2
errV = 0.001

# Getting current values from Ohm's law (I = V/R)
C = [x/R for x in V]
print(C)

#Error of current, added in quadrature with errors of V and R


#print(err3)
f = plt.figure(figsize=(8,6))
plt.plot(C, I3)

plt.show()