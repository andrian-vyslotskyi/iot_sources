import time
import ASUS.GPIO as GPIO
from common.configs import DummyConfig
from common.handler import ConsoleHandler

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

config = DummyConfig()
handler = ConsoleHandler()

pin = config.rain_pin()


def water_detected(pin):
    if GPIO.input(pin) == GPIO.LOW:
        handler.handle_water(time.time())


GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.BOTH, callback=water_detected(pin), bouncetime=500)

# cycle to keep main process alive
while True:
    time.sleep(1000)
