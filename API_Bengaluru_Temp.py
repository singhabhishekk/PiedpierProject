import requests
import json

response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Bangalore,IN&appid=d1d9aaef451587b27b3f9fc29d75899d")


obj = json.loads(response.content)
float_temp = float(obj['main']['temp'])
float_temp_degreeC = float(float_temp - 273)
print ("Outside Temperature in Bangalore is: " ,str(float_temp_degreeC) + " Celsius")
