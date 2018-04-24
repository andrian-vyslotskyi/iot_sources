from pika import BlockingConnection, SelectConnection, ConnectionParameters, BasicProperties

from common.handler import Handler
from serializations import serialize_as_string


class RabbitHandler(Handler):
    def __init__(self, host, port, exchange, persistent, is_blocking):
        parameters = ConnectionParameters(host=host, port=port)
        if is_blocking:
            self.connection = BlockingConnection(parameters)
        else:
            self.connection = SelectConnection(parameters)

        self.channel = self.connection.channel()
        self.exchange = exchange

        if persistent:
            self.properties = BasicProperties(delivery_mode=2)
        else:
            self.properties = BasicProperties(delivery_mode=1)

    def handle_message(self, routing_key, body):
        self.channel.basic_publish(self.exchange,
                                   routing_key=routing_key,
                                   properties=self.properties,
                                   body=body)

    def handle_light(self, timestamp, is_light):
        pass

    def handle_temperature(self, timestamp, temperature, humidity):
        pass

    def handle_water(self, timestamp, is_water):
        pass

    def handle_soil(self, timestamp, is_wet):
        pass


# pub\sub model without channels or routing keys
# serialized data contains some key
# consumers should parse key from data
class FanoutRabbitHandler(RabbitHandler):
    def __init__(self, host, port, exchange, machine, persistent=True, is_blocking=True):
        super(FanoutRabbitHandler, self).__init__(host, port, exchange, persistent, is_blocking)

        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
        self.machine = machine

    def handle_light(self, timestamp, is_light):
        self.handle_message(routing_key='',
                            body=serialize_as_string(':', timestamp, self.machine, 'light', is_light))

    def handle_soil(self, timestamp, is_wet):
        self.handle_message(routing_key='',
                            body=serialize_as_string(':', timestamp, self.machine, 'soil', is_wet))

    def handle_water(self, timestamp, is_water):
        self.handle_message(routing_key='',
                            body=serialize_as_string(':', timestamp, self.machine, 'water', is_water))

    def handle_temperature(self, timestamp, temperature, humidity):
        self.handle_message(routing_key='',
                            body=serialize_as_string(':', timestamp, self.machine, 'temperature', temperature))

        self.handle_message(routing_key='',
                            body=serialize_as_string(':', timestamp, self.machine, 'humidity', humidity))


# model with routing based on machine name and key (name of sensor)
# 1 topic = 1 queue = 1 consumer for pub\sub (queue)
class TopicRabbitHandler(RabbitHandler):
    def __init__(self, host, port, exchange, machine, persistent=True, is_blocking=True):
        super(TopicRabbitHandler, self).__init__(host, port, exchange, persistent, is_blocking)

        self.channel.exchange_declare(exchange=exchange, exchange_type='topic')
        self.machine = machine

    def handle_light(self, timestamp, is_light):
        routing = self.machine + '.light'
        self.handle_message(routing_key=routing,
                            body=serialize_as_string(':', timestamp, is_light))

    def handle_soil(self, timestamp, is_wet):
        routing = self.machine + '.soil'
        self.handle_message(routing_key=routing,
                            body=serialize_as_string(':', timestamp, is_wet))

    def handle_water(self, timestamp, is_water):
        routing = self.machine + '.water'
        self.handle_message(routing_key=routing,
                            body=serialize_as_string(':', timestamp, is_water))

    def handle_temperature(self, timestamp, temperature, humidity):
        routing_temperature = self.machine + '.temperature'
        self.handle_message(routing_key=routing_temperature,
                            body=serialize_as_string(':', timestamp, temperature))

        routing_humidity = self.machine + '.humidity'
        self.handle_message(routing_key=routing_humidity,
                            body=serialize_as_string(':', timestamp, humidity))


# model that can have multiple queues for 1 routing_key
# sensor name is routing key for such model
class DirectRabbitHandler(RabbitHandler):
    def __init__(self, host, port, exchange, machine, persistent=True, is_blocking=True):
        super(DirectRabbitHandler, self).__init__(host, port, exchange, persistent, is_blocking)

        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')
        self.machine = machine

    def handle_light(self, timestamp, is_light):
        self.handle_message(routing_key='light',
                            body=serialize_as_string(':', timestamp, self.machine, is_light))

    def handle_temperature(self, timestamp, temperature, humidity):
        self.handle_message(routing_key='temperature',
                            body=serialize_as_string(':', timestamp, self.machine, temperature))

        self.handle_message(routing_key='humidity',
                            body=serialize_as_string(':', timestamp, self.machine, humidity))

    def handle_water(self, timestamp, is_water):
        self.handle_message(routing_key='water',
                            body=serialize_as_string(':', timestamp, self.machine, is_water))

    def handle_soil(self, timestamp, is_wet):
        self.handle_message(routing_key='soil',
                            body=serialize_as_string(':', timestamp, self.machine, is_wet))
