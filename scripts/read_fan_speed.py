import RPi.GPIO as GPIO
import time
import os

# Pin configuration
FAN_TACH_IN_PIN = int( os.getenv( 'FAN_TACH_IN_PIN', 24 ) )           # Fan's tachometer output pin
FAN_TACH_PULSE_PER_REV = int( os.getenv( 'FAN_TACH_PULSE_PER_REV', 2 ) )    # Pulses per Revolution
FAN_TACH_REFRESH_TIME = int( os.getenv( 'FAN_TACH_REFRESH_TIME', 1 ) )                 # [s] Time to wait between each refresh
print( "FAN_TACH_IN_PIN: %(i)s; FAN_TACH_PULSE_PER_REV: %(p)s; FAN_TACH_REFRESH_TIME: %(t)s" % { 'i': type( FAN_TACH_IN_PIN ), 'p': FAN_TACH_PULSE_PER_REV, 't': FAN_TACH_REFRESH_TIME } )

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(FAN_TACH_IN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull up to 3.3V

# Setup variables
t = time.time()
rpm = 0

# Caculate pulse frequency and RPM
def fell(n):
    global t
    global rpm

    dt = time.time() - t
    if dt < 0.005: return # Reject spuriously short pulses

    freq = 1 / dt
    rpm = (freq / FAN_TACH_PULSE_PER_REV) * 60
    t = time.time()

# Add event to detect
GPIO.add_event_detect(FAN_TACH_IN_PIN, GPIO.FALLING, fell)

try:
    while True:
        print("%.f RPM" % rpm)
        rpm = 0
        time.sleep(FAN_TACH_REFRESH_TIME)   # Detect every second

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    GPIO.cleanup() # resets all GPIO ports used by this function