import RPi.GPIO as GPIO
import time

PIR_PIN = 17  # gpio17 = physical pin 11

# set up gpio mode and pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

print("\n===== testing pir sensor =====")
print("wave your hand in front of the sensor ...")
print("press ctrl+c to stop")
print("pir is connected to gpio 17")  

try:
    while True:
        # check if motion is detected
        if GPIO.input(PIR_PIN):
            print("  motion detected  ") 
        else:
            print("\n~ no motion ~") 
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n\n*** test stopped ***") 
    GPIO.cleanup()