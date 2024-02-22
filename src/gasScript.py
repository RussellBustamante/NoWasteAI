import time, Adafruit_MCP3008
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import numpy as np
from numpy.polynomial import Polynomial

#using physical pin 11 to blink an LED

def getSense():
    GPIO.setmode(GPIO.BOARD)
    chan_list = [11]
    GPIO.setup(chan_list, GPIO.OUT)
    #Following commands control the state of the output
    #pin = 11


    # Hardware SPI configuration:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
    # get reading from adc 
    # mcp.read_adc(adc_channel)

    # Fit PPM to Ratio
    x = [200, 500, 800, 1000, 1500, 2000, 3000, 5000, 100000]
    y = [3, 2.2, 1.9, 1.8, 1.5, 1.3, 1.2, 0.9, 0.7]

    plot = Polynomial.fit(x,y,4)

    def blinkLED(times, pin, interval):
        for i in range(times):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(interval/2)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(interval/2)

    def gasSensor(channel):
        return (mcp.read_adc(channel))
            
    while True: 
        #R0 = 0.424 #in air
        sensorValue = 0
        for i in range(100):
            sensorValue =sensorValue + gasSensor(0)
            time.sleep(0.05) # collects gas samples over 5s. 
        sensorValue = sensorValue/100
        print(sensorValue)
        break
if __name__ == "__main__":
    result = getSense()
    print(result)
    """
    sensorVolt = 5 * sensorValue/1024
    RSgas = (5.0-sensorVolt)/sensorVolt/10
    ratio = RSgas/R0
    print(ratio)

    ppmArray = (plot - ratio).roots()
    ppmBool = np.isreal(ppmArray)
    ppm = ((ppmArray.real)[0])/7
    print(ppm)
    time.sleep(1)"""

    """R0 = 0.4899 #in air
    sensorValue = 0
    for i in range(100):
        sensorValue =sensorValue + gasSensor(0)
    sensorValue = sensorValue/100
    sensorVolt = 5 * sensorValue/1024
    RSgas = (5.0-sensorVolt)/sensorVolt/10
    ratio = RSgas/R0
    print(ratio)

    ppm = (ratio-1.7521)/(-1.113*10**-5)
    print(ppm)
    time.sleep(5)"""
