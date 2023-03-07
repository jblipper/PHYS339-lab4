# -*- coding: utf-8 -*-
"""
This code requires:
    1) <laserClass2022.py> to be in the same folder as this code
    2) <laser2022.ino> to be uploaded to the Arduino

It does not imply what you need to do, merely implements a simple
experiment that gives an example interaction with the Arduino.

Be sure to wire your laser control card up to the true DAC.

# Original code by Mark Orchard-Webb < 2017.12.31
# Updated to Python 3 and commented by Gregory Bell 2021.04.30

The first time this code runs, the plot window stays behind the Spyder IDE
window. If the initial plot window is closed, on subsequent runs it will appear
in front of the IDE. Otherwise, subsequent plots will be overlaid in the
initial plot window.

robert.turner@mcgill.ca
2021.12.20
"""

import matplotlib.pyplot as plt
import laserClass2022
import numpy as np

#-----------------------------------------------------------------------------!
# Ensure that this string contains the correct COM port number!
#device = 'COM3'
device = "/dev/ttyACM0"

# Create an instance of the "Arduino" class, which communicates through
# the serial port with the Arduino
a = laserClass2022.Arduino(device = device, verbose = 0)

intensities = np.linspace(0, 4095, 1024)
out = np.zeros(len(intensities))

for n, i in enumerate(intensities):
    # The number of measurements you wish you take, this variable also specifies
    # the number of steps taken by the motor
    steps = 3
    # This has to be calibrated by you
    degsPerStep = 1
    # Laser control voltage
    intensity = str(i)
    a.send("LASER " + intensity)
    # Total number of steps
    a.send(f"STEPS {steps}")
    # Delay time before reading value (ms), >4 recommended
    a.send("DELAY 4")
    # Start the stepping/reading
    a.send("START")
    # Sends a signal to change a variable on the Arduino such that the motor
    # stops after one full set of steps is executed
    a.send("STOP")

    # Declare arrays for storing data.
    arryAll = []
    # Step indexes
    stepCounts = []
    # ADC readings
    adcValues = []

    # Greg writes:
    # "I'm not sure the point of this, the index is not incremented,
    # maybe set it to 10 if leaving the loop after one time is wanted,
    # it is used in the graphing code"
    index = -1
    for k in range(steps):
        # get a readline
        resp = a.getResp()
        # if the length of the response is 9 and the 4 index of it is :
        if 9 == len(resp) and resp[4] == ':':
            # Append raw response to array of raw serial data
            arryAll.append(resp)
            print("Got response ", resp)

            # Split the response by the colon delimiter
            words = str.split(resp, ":")

            # Note step count and append to appropriate array
            step = int(words[0])
            stepCounts.append(step)

            # Note A0 ADC value and append to appropriate array
            adc = int(words[1])
            adcValues.append(adc)
        else:
            print(f"Unexpected response: {resp}")
            print(f"Length: {len(resp)}")
        # could leave loop after one time if this were set to 10
        if 10 == index:
            # leave loop
            break

    # multiply array of stepCounts by degsperstep
    stepCountsCal = np.array(stepCounts) * degsPerStep
    # make array of adcvalues
    adcValuesnp = np.array(adcValues)

    # Basic plot of ADC value per calibrated degree
    # Useful for a quick check of th data's quality
    #plt.plot(stepCountsCal, adcValuesnp)
    #plt.title("{}".format(intensity))

    # Shuts down laser
    a.send("LASER 0")

    print(np.mean(adcValuesnp))
    out[n] = np.mean(adcValuesnp)

print("Laser should have turned off by now")
data = np.concatenate((intensities[:,np.newaxis], out[:,np.newaxis]), axis=1)
np.savetxt("./data/detector_response_2.csv", data, delimiter=",")
plt.plot(intensities, out)
plt.show()

# Closes port
a.closePort()
