import ASUS.GPIO as GPIO
import time
from common.configs import DummyConfig
from common.handler import ConsoleHandler

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

config = DummyConfig()
handler = ConsoleHandler()

pin = config.light_pin()


def light_changed(pin):
    is_light = GPIO.input(pin) == GPIO.LOW
    handler.handle_light(time.time(), is_light)


GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.BOTH, callback=light_changed, bouncetime=100)

# cycle to keep main process alive
while True:
    time.sleep(1000)
