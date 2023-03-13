# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 18:23:51 2023

@author: Bhuvan
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf, expit



plt.rcParams.update({'font.size': 18})

file = 'detector_response.csv'
data = np.genfromtxt(file, delimiter = ",")
x = data[:,0]
y = data[:,1]


def Erf(x,a,b,c,h):
    return a*erf(c*(x-h))+b


popt, pcov = curve_fit(Erf, x, y, p0 = [200,200,1,1000])
print('Erf paramters:', popt)


def Arctan(x,a,b,c,h):
    return a*np.arctan(x*(x-h))+b


popt1, pcov1 = curve_fit(Arctan, x, y, p0 = [200,250,200,1250])
print('Arctan paramters:', popt1)


def Step(x,a,b,c,h):
    return a*expit((x-h)*c)+b


popt2, pcov2 = curve_fit(Step, x, y, p0 = [500,1,200,1000])
print('Step function paramters:', popt2)



chierf = chisquare(y, Erf(x, *popt))
chiarctan = chisquare(y, Arctan(x, *popt1))
chistep = chisquare(y, Step(x, *popt2))
                   
print('Chi2 for erf is:', chierf)
print('Chi2 for arctan is:', chiarctan)
print('Chi2 for step is:', chistep)

def chi2(observed, expected, err):
    return np.sum((observed - expected)**2/err**2)

chi2(mean, cos_squared(deg, popt[0], popt[1]), err)



plt.plot(x, y)
plt.plot(x, Erf(x, *popt), 'darkorange', label = 'Error function fit')
plt.plot(x, Arctan(x, *popt1), 'tab:olive', label = 'Arctan fit')
plt.plot(x, Step(x, *popt2), 'k', label = 'Step function fit')
plt.title('Calibration Curve of Detector')
plt.xlabel('Input Laser Intensity')
plt.ylabel('Detected Laser Intensity')
plt.legend(fontsize = 14)
plt.show()


