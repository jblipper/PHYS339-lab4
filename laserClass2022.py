# -*- coding: utf-8 -*-
"""
This should be quite familiar by now. A simple script with some error checking
to open an arduino device and send/receive data from it.

# Original code by Mark Orchard-Webb < 2017.12.31
# Updated to Python 3 and commented by Gregory Bell 2021.04.30

Double hash marks <##> precede snippets of code which were left commented
These will be reomved in the future.

robert.turner@mcgill.ca
2021.12.20

"""

import serial


class Arduino:
    # device is COM port used with arduino
    def __init__(self, device = 'COM3', verbose = 0):
        # get verbose instance attribute
        self.verbose = verbose
        if verbose: print("introArduino class creator: Verbose mode activated")
        # you may have to adjust range(1,10) depending on your COM ports
        ##for i in range(2,10):
            ##device = "COM%d" % (i) 
            ##device = f"COM{i}" 
        try:
            # serial port instance with baudrate and timeout set
            self.device = serial.Serial(device, baudrate = 115200, timeout = 1.0)
            ##if verbose: print("Found device at %s" % (device))
            if verbose: print(f"Found device at {device}")
            #break
        except:
            print('Device not found')
            #continue
        # reboot Arduino
        self.device.setDTR(1);
        self.device.setDTR(0);
        self.device.setDTR(1);
        exception_count = 0
        attempts = 0
        # runs until break or return
        while True:
            try:
                # if the first part of the serial port response is this
                if "LASER 2022" == self.getResp()[0:10]:
                    if verbose: print("Arduino is communicating")
                    # leaves loop because it leaves the init function
                    return
            except:
                if self.verbose: print("Exception")
                exception_count += 1
                
            # redundant to have both exception_count
            # and attempts counting, but it works
            # redundant to have both exception_count and attempts counting,
            # but it works
            attempts += 1
            if 5 == attempts:
                ##print("Unable to communicate with Arduino...%d exceptions" % (exception_count))
                print(f"Unable to communicate with Arduino...{exception_count} exceptions")
                # leave loop
                break

    # changed str to strr, str is a built-in type
    def send(self, strr):
        ##self.device.write("%s\n" % (str))
        # added for arduino code
        strr = strr + '\n'
        # write to serial port after encoding to bytes
        self.device.write(strr.encode())
        ##if self.verbose: print("Sent '%s'" % (str))
        if self.verbose: print(f"Sent '{strr}'", end=' ')

    def getResp(self):
        if self.verbose: print("Waiting for response...", end = ' ')
        # readline of serial port, bytes decoded, splits along \r\n and first element is taken
        strr = self.device.readline().decode().split('\r\n')[0]
        if self.verbose: print(f"Got response: '{strr}'", end=' ')
        return strr

    def closePort(self):
        # close serial port
        self.device.close()
        print("Port is now closed")
