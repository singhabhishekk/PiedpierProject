#!/usr/bin/env python
import os
import paho.mqtt.client as mqtt
import time
import redis
import RPi.GPIO as GPIO
import SegmentDisplay
import ADC0832


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)# Numbers pins by physical location
GPIO.setup(29, GPIO.OUT)
##GPIO.setup(18, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)# Set pin mode as output
GPIO.output(29, GPIO.HIGH)
GPIO.output(31, GPIO.HIGH)

BZRPin = 11
GPIO.setup(BZRPin, GPIO.OUT) # Set pin mode as output
GPIO.output(BZRPin, GPIO.LOW)
p = GPIO.PWM(BZRPin, 50) # init frequency: 50HZ


r = redis.Redis(host='redis-17178.c8.us-east-1-4.ec2.cloud.redislabs.com', port='***', password='*****')

#MQTT 
broker_address="192.168.0.102"
client = mqtt.Client("tz23")
client.connect(broker_address)

# Reads temperature from sensor and prints to stdout

def readSensor():
	tfile = open("/sys/bus/w1/devices/28-0316573129ff/w1_slave")
	text = tfile.read()
	tfile.close()
	secondline = text.split("\n")[1]
	temperaturedata = secondline.split(" ")[9]
	temperature = float(temperaturedata[2:])
	temperature = temperature / 1000
	client.publish("rpitempsensorabhi",temperature)
	print 'Temperature is :', str(temperature)+' Celsius'
##        GPIO.setwarnings(False)
##        GPIO.setmode(GPIO.BOARD)# Numbers pins by physical location
#	GPIO.output(29, GPIO.HIGH)
#	GPIO.output(31, GPIO.HIGH)
	

# Logic for LED and buzzer. RED LED for high temperatute (more than 25)

	if temperature < 30:	
            GPIO.output(29, GPIO.LOW)
            time.sleep(0.5)
            GPIO.output(31, GPIO.HIGH)
            time.sleep(0.5)
            
        if temperature > 30:
            GPIO.output(29, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(31, GPIO.LOW)
            time.sleep(0.5)
            p.start(50)
            for f in range(220, 880, 50):
			p.ChangeFrequency(f)
			time.sleep(0.1)
#	    GPIO.output(BZRPin, GPIO.LOW)
        time.sleep(1)
        return temperature
    
## Code for soil humidity
    
def Soil_init():
	ADC0832.setup()

def Soil_loop():
	while True:
		res = ADC0832.getResult(0)
		moisture = 255 - res
		pcntg= float((moisture*100)/255)
		client.publish("rpisoilhumsensorabhi",pcntg)
#		print ('moisture is: ' '%.0f' % pcntg +'%')
#		print ('analog value: %03d  moisture is: %d' %(res, moisture))
		time.sleep(.5)

		return pcntg

def Light_init():
	ADC0832.setup()

def Light_loop():
	while True:

		res = ADC0832.getResult(1)
		light= float((res*100)/255)
		print ('Brightness is: ' '%.0f' % light +'%')
		r.set('Brightness', light)
		time.sleep(2)
		return light
#	r.set('Temp', temperature)
#	return str(temperature)
	
		#print "test"
#	print ("Current temperature : %0.3f C" % temperature)



#def loop():
while True:
#        GPIO.cleanup()
    reading = readSensor()
    Soil_init()
    Soil_hum = Soil_loop()
    Light_init()
    Light_loop()
    SegmentDisplay.numberDisplay_dec(reading)
    time.sleep(.5)
    p.stop()
    print ('Soil humidity is: ' '%.0f' % Soil_hum +'%')
    
    

#    GPIO.cleanup()
#		mqtt.single("rpitempsensorabhi",reading,hostname="test.mosquitto.org")
#		print (reading)
#                templateData = {
#                    'temperature'  : reading
#                    }
#                return render_template('index.html', **templateData)
#                time.sleep(1)


# Main starts here
#if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=80, debug=True)

