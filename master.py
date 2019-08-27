"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime
import time
import os
import paho.mqtt.client as paho


from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()


def on_message(mqttc, obj, msg):
    print(msg.topic)
    print(msg.payload.decode("utf-8"))
    scheduler.reschedule_job("surya", trigger='interval', seconds=int(msg.payload.decode("utf-8")))

#MQTT credentials
client = paho.Client("HYP-MASTER-RASPI")
broker = '165.22.209.7' #server ip
port = 1883 #default mqtt port
try:
    client.connect(broker, 1883, 60)
except: 
    print("oops") 
    
client.on_message = on_message
client.is_connected = True
client.subscribe('hyp/ctrl')
client.loop_start()





def tick():
    print('Tick! The time is: %s' % datetime.now())
    try:
        client.publish('test',"i am in a pub..")
    except expression :
        print(expression)
    


if __name__ == '__main__':
    scheduler.add_job(tick, 'interval', seconds=5, id="surya")
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        a = input("Enter your name")
        if a=="john":
            scheduler.reschedule_job("surya", trigger='interval', seconds=1)
            print(a)
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()