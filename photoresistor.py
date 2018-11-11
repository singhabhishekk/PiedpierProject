#!/usr/bin/env python
import ADC0832
import time

def init():
	ADC0832.setup()

def loop():
	while True:

		res = ADC0832.getResult(1)
		light= float((res*100)/255)
		print ('Brightness is: ' '%.0f' % light +'%')
		time.sleep(2)
            
###		print res
##		if res < 0:
##			res = 0
##		if res > 100:
##			res = 100
###		print 'res = %d' % res
		time.sleep(2)

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt: 
		ADC0832.destroy()
		print ('The end !')
