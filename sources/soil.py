import ASUS.GPIO as GPIO
import time
from common.configs import DummyConfig
from common.handler import ConsoleHandler

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

config = DummyConfig()
handler = ConsoleHandler()

pin = config.moisture_pin()


def moisture_changed(pin):
    is_wet = GPIO.input(pin) == GPIO.LOW
    handler.handle_soil(time.time(), is_wet)


GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.BOTH, callback=moisture_changed, bouncetime=200)

# cycle to keep main process alive
while True:
    time.sleep(100)