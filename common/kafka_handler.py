from kafka import KafkaProducer

from common.handler import Handler


class KafkaHandler(Handler):
    def __init__(self, bootstrap, machine, acks=1, retries=0):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap,
                                      client_id=machine,
                                      retries=retries,
                                      acks=acks)

    def handle_light(self, timestamp, is_light):
        self.producer.send('light', key=timestamp, value=is_light)

    def handle_temperature(self, timestamp, temperature, humidity):
        self.producer.send('temperature', key=timestamp, value=temperature)
        self.producer.send('humidity', key=timestamp, value=humidity)

    def handle_water(self, timestamp, is_water):
        self.producer.send('water', key=timestamp, value=is_water)

    def handle_soil(self, timestamp, is_wet):
        self.producer.send('soil', key=timestamp, value=is_wet)
