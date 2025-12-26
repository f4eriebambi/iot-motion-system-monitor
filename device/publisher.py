import time
import os
import RPi.GPIO as GPIO
from datetime import datetime
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# gpio configuration
PIR_PIN = 17  # gpio17 = physical pin 11

# set up gpio mode and pin for pir sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# pubnub configuration
pnconfig = PNConfiguration()
pnconfig.publish_key = os.getenv("PUBNUB_PUBLISH_KEY")
pnconfig.subscribe_key = os.getenv("PUBNUB_SUBSCRIBE_KEY")
pnconfig.uuid = os.getenv("PUBNUB_UUID")

pubnub = PubNub(pnconfig)

CHANNEL = os.getenv("PUBNUB_CHANNEL")

def get_cpu_temperature():
    # returns cpu temperature rounded to one decimal place
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp_c = int(f.read()) / 1000.0
    return round(temp_c, 1)

print("\n==== starting motion publisher ====")
print("waiting for motion ...")
print("press ctrl+c to stop")

try:
    while True:
        if GPIO.input(PIR_PIN):  # check if motion is detected
            cpu_temp = get_cpu_temperature()  # get current cpu temperature

            # create payload to send to pubnub
            payload = {
                "event": "motion_detected",
                "cpu_temp": cpu_temp,
                "timestamp": datetime.now().isoformat(),
                "device": "raspberry-pi-zero-w"
            }

            # publish the payload to the pubnub channel
            pubnub.publish().channel(CHANNEL).message(payload).sync()

            # print motion detection message
            print(f"\nmotion detected | cpu temp: {cpu_temp}°C")
            time.sleep(2)

        time.sleep(0.2)

except KeyboardInterrupt:
    print("\n\n*** publisher stopped ***")
    GPIO.cleanup()