#!/usr/bin/env python
import ADC0832
import time

def Soil_init():
	ADC0832.setup()

def Soil_loop():
	while True:
		res = ADC0832.getResult()
		moisture = 255 - res
		pcntg= float((moisture*100)/255)
		print ('moisture is: ' '%.0f' % pcntg +'%')
#		print ('analog value: %03d  moisture is: %d' %(res, moisture))
		time.sleep(2)
		return pcntg
		

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()
		print ('The end !')
