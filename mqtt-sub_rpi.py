import paho.mqtt.client as mqtt
import time
import redis


r = redis.Redis(host='redis-17178.c8.us-east-1-4.ec2.cloud.redislabs.com', port='***', password='****')


def on_message(client, userdata, message):
    m = str(message.payload.decode("utf-8"))
    print ("message got " + m)
    r.set('MQTT_TEMP',m)
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


broker_address="192.168.0.102"
print("creating new instance")
client = mqtt.Client("s44") #create new instance
client.on_message=on_message #attach function to callback
print ("connecting to broker")
client.connect(broker_address) #connect to broker
print ("not yet connected")
client.loop_start() #start the loop
print ("loop started")

while True:
    client.subscribe("rpitempsensorabhi")
    print ("loop started subscribing")### USE YOUR OWN TOPIC NAME
    time.sleep(5)
    # wait

client.loop_stop()
