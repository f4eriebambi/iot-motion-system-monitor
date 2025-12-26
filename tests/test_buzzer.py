from gpiozero import PWMOutputDevice
from time import sleep

# initialize pwm output on gpio 24 for a passive buzzer
buzzer = PWMOutputDevice(24)

print("\n===== testing buzzer =====") 
print("press ctrl+c to stop")
print("buzzer is connected to gpio 24") 

try:
    while True:
        # set the buzzer sound level (4000 = high pitch, 2000 = lower pitch)
        buzzer.frequency = 4000

        # set buzzer volume (1.0 = loudest, 0.2 = quiet)
        buzzer.value = 0.5

        print("~ playing sound ~")
        sleep(1)

        # turn the buzzer off
        buzzer.off()
        print("  sound stopped")
        sleep(1)  

except KeyboardInterrupt:
    print("\n\n*** test stopped ***") 
    buzzer.off()