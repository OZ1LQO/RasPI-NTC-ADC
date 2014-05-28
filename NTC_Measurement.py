
#Linearized B3470 NTC temperature measurement using an A/D converter from abelectronics.
# http://www.abelectronics.co.uk/products/3/Raspberry-Pi/39/ADC-DAC-Pi-Raspberry-Pi-ADC-and-DAC-expansion-board
#Linearization resistor and series resistor was calculated in a spreadsheet
#R_lin=2K, R_series=2.2k. Power supply is selectable from 5V or 3.3V
#This script uses spidev and scipy which may have to be installed if not included already in the python installation.
#The script is written for Python 2.7
#OZ1LQO 2014.05.26


import spidev
import time
from scipy import interpolate


#Setting up A/D Converter
spi = spidev.SpiDev()
spi.open(0,0)
     

def get_adc(channel):
    """This function handles reading from the ADC.
    Depending on the ADC module and adjoining libraries,
    this may have to be rewritten accordingly.
    The MCP3002 has a 3.3V rail"""
        
    # Only 2 channels 0 and 1 else return -1
    if ((channel > 1) or (channel < 0)):
        return -1
    r = spi.xfer2([1,(2+channel)<<6,0])
           
    ret = ((r[1]&0x0F) << 8) + (r[2])
    
    return ret*3.3/4096 #compensate for supply voltage and resolution for this specific ADC





#Define voltage vs. temperature arrays for the interpolate function
#X should always be ascending

#for 3.3V supply:
#vntc_a is based on the theoretical thermistor formulas (see spreadsheet)
#vntc_b is based on the on actual measurements of the thermistor behaviour.
vntc_a=[0.77, 0.80, 0.85, 0.90, 0.95, 1.0, 1.05, 1.10, 1.15, 1.20, 1.24, 1.28, 1.32, 1.35, 1.38, 1.41, 1.44, 1.46, 1.47, 1.49, 1.50]
vntc_b=[0.74, 0.78, 0.82, 0.87, 0.93, 0.98, 1.03, 1.08, 1.13, 1.17, 1.22, 1.26, 1.3, 1.33, 1.37, 1.41, 1.43, 1.45, 1.46, 1.47, 1.50]

#for 5.0V supply:
#vntc_c is based on the theoretical thermistor formulas (see spreadsheet)
#vntc_d is based on the on actual measurements of the thermistor behaviour.
vntc_c=[1.16, 1.21, 1.29, 1.36, 1.44, 1.52, 1.60, 1.67, 1.74, 1.81, 1.88, 1.94, 2.00, 2.05, 2.10, 2.14, 2.17, 2.21, 2.23, 2.26, 2.27]
vntc_d=[1.12, 1.18, 1.25, 1.32, 1.40, 1.48, 1.56, 1.63, 1.71, 1.78, 1.85, 1.91, 1.97, 2.02, 2.07, 2.13, 2.16, 2.19, 2.22, 2.23, 2.27]

#Array with the corresponding temperature range in deg C
temperature_y=[98,95,90,85,80,75,70,65,60,55,50,45,40,35,30,25,20,15,10,5,1]



# -MAIN SCRIPT PART-
#Greet the user
print """Welcome to the Rasperry PI NTC Thermistor demo! (OZ1LQO 2014.05.27)
This demo shows how to use a linearized NTC Thermistor to measure the temperature.
See the calculation spreadsheet to learn about the linearization calculations.
You have two options:
1) Select supply (3.3 or 5V) for the sensor circuit
2) Select if you want to use a theoretical model for the Thermistor or if you want to
   use a real world measured characteristic"""

supply=raw_input("\nWhat do you want, 1: 3.3V supply or 2: 5V ")
model=raw_input("\nDo you want to use the theoretical model (1) or the measured characteristic (2) ")

#select the right array based on the inputs
if supply=='1':
    if model=='1':
        voltage_x=vntc_a
    else:
        voltage_x=vntc_b
elif supply=='2':
    if model=='1':
        voltage_x=vntc_c
    else:
        voltage_x=vntc_d

#define the temp function, interpolated between the two arrays. Use cubic approximation
#use scipy.interpolate.interp1d for this
temp=interpolate.interp1d(voltage_x,temperature_y,kind='cubic')


   
 

#Do 10 measurements at 1 second interval on ADC 0 based on the chosen parameters 

for i in xrange(10):
    level=get_adc(0)#Get ADC voltage
    #print "Level: ", level
    measured_temp=temp(level) #Calculate corresponding temperature
    print "%.2f" % round(measured_temp,2) #Print it using two decimals
    time.sleep(1)
    





    


