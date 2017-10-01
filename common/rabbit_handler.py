from pika import BlockingConnection, SelectConnection, ConnectionParameters, BasicProperties

from common.handler import Handler


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
    def __init__(self, host, port, exchange, persistent=True, is_blocking=True):
        super(FanoutRabbitHandler, self).__init__(host, port, exchange, persistent, is_blocking)

        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    def handle_light(self, timestamp, is_light):
        self.handle_message('', '')
        # todo: serialization of data

    def handle_soil(self, timestamp, is_wet):
        self.handle_message('', '')

    def handle_water(self, timestamp, is_water):
        self.handle_message('', '')

    def handle_temperature(self, timestamp, temperature, humidity):
        self.handle_message('', '')


# model with routing based on machine name and key (name of sensor)
# 1 topic = 1 queue = 1 consumer for pub\sub (queue)
class TopicRabbitHandler(RabbitHandler):
    def __init__(self, host, port, exchange, machine, persistent=True, is_blocking=True):
        super(TopicRabbitHandler, self).__init__(host, port, exchange, persistent, is_blocking)

        self.channel.exchange_declare(exchange=exchange, exchange_type='topic')
        self.machine = machine

    def handle_light(self, timestamp, is_light):
        routing = self.machine + '.light'
        self.handle_message(routing, '')
        # todo: serialization of data

    def handle_soil(self, timestamp, is_wet):
        routing = self.machine + '.soil'
        self.handle_message(routing, '')
        # todo: serialization of data

    def handle_water(self, timestamp, is_water):
        routing = self.machine + '.water'
        self.handle_message(routing, '')
        # todo: serialization of data

    def handle_temperature(self, timestamp, temperature, humidity):
        routing_temperature = self.machine + '.temperature'
        self.handle_message(routing_temperature, '')

        routing_humidity = self.machine + '.humidity'
        self.handle_message(routing_humidity, '')
        # todo: serialization of data


# model that can have multiple queues for 1 routing_key
# sensor name is routing key for such model
class DirectRabbitHandler(RabbitHandler):
    def __init__(self, host, port, exchange, persistent=True, is_blocking=True):
        super(DirectRabbitHandler, self).__init__(host, port, exchange, persistent, is_blocking)

        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')

    def handle_light(self, timestamp, is_light):
        self.handle_message('light', '')
        # todo: serialization of data

    def handle_temperature(self, timestamp, temperature, humidity):
        self.handle_message('temperature', '')

        self.handle_message(humidity, '')
        # todo: serialization of data

    def handle_water(self, timestamp, is_water):
        self.handle_message('water', '')
        # todo: serialization of data

    def handle_soil(self, timestamp, is_wet):
        self.handle_message('soil', '')
        # todo: serialization of data
