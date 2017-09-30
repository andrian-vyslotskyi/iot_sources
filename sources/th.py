import time
import dht11
import ASUS.GPIO as GPIO
from common.configs import DummyConfig
from common.handler import ConsoleHandler

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

config = DummyConfig()
handler = ConsoleHandler()

pin = config.temperature_pin()

GPIO.setup(pin, GPIO.IN)
sensor = dht11.DHT11(pin, GPIO)
while True:
    result = sensor.read()
    if result.is_valid():
        ts = time.time()  # in seconds
        handler.handle_temperature(ts, result.temperature, result.humidity)
