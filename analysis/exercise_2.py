# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:06:49 2023

@author: Bhuvan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf
from scipy.stats import chisquare
import os

plt.rcParams.update({'font.size': 22})

I1 = np.array([0,300,600,900,1200,1500,1800,2100,2400,2700,3000,3900,4095])
I2 = np.array([i for i in range(0,2500,100)])
I3 = np.array([i for i in range(0,2500,100)], dtype = float)

R = 100
errR = 10

V1 = np.array([0.002,0,0,0.369,0,0,0.737,0,0,1.109,0,0,1.470,0,0,1.656,0,0,1.657,0,0,1.657,0,0,1.657])
V2 = np.array([0.002,0.129,0.247,0.369,0.493,0.616,0.737,0.857,0.982,1.109,1.232,1.349,1.471,1.596, 1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660,1.660])
V3 = np.array([0.003,0.129,0.246,0.369,0.493,0.617,0.737,0.857,0.982,1.109,1.232,1.349,1.471,1.596, 1.661,1.662,1.662,1.662,1.662,1.662,1.662,1.662,1.662,1.662,1.662])
V = (V2+V3)/2
errV = 0.01
print(V)
# Getting current values from Ohm's law (I = V/R)
C = np.array([x/R for x in V], dtype = float)
I_new = [2.66233854e+02*erf(2.11948436e-02*(x-1.24771088e+03))+2.67390488e+02 for x in I3]
print(I_new)
#Error of current, added in quadrature with errors of V and R
errx = []
for i in range(0,25):
    Cerr = C[i]*((errV/V[i]) + (errR/R))
    errx.append(Cerr)
    
def LinearPiecewise(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

#def LinearPiecewise(x, x0, a, b, c):
    #y = a*np.abs(x-x0) + b*x + c
    #return y

popt, pcov = curve_fit(LinearPiecewise, C, I_new, p0=[0, 0, 1.0, 100.0])



f = plt.figure(figsize=(8,6))
xd = np.linspace(0, max(C), 100)
#plt.plot(C_new, I3)
plt.errorbar(C, I_new, xerr=errx, capsize = 5, capthick = 1.5, elinewidth = 3)
plt.plot(xd, LinearPiecewise(xd, *popt), label = 'Piecewise linear fit')
plt.title('Input Laser Intensity vs. Current')
plt.xlabel('Current(A)')
plt.ylabel('Input Laser Intensity(arb. units)')
plt.legend(fontsize = 18)
plt.show()
print(popt)
    

#print(err3)
#f = plt.figure(figsize=(8,6))
#plt.errorbar(C, I3, xerr=errx, capsize = 5, capthick = 1.5, elinewidth=3)
#plt.title('Laser Intensity vs. Current')
#plt.xlabel('Current(A)')
#plt.ylabel('Laser Intensity(arb. units)')

plt.show()