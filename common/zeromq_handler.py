import zmq

from common.handler import Handler


class ZeroMqHandler(Handler):
    def __init__(self, bind_address):
        self.ctx = zmq.Context()
        self.pub_socket = self.ctx.socket(zmq.PUB)  # constants.constants.
        self.pub_socket.bind(bind_address)

    def handle_light(self, timestamp, is_light):
        self.pub_socket.send_multipart(['light', {timestamp, is_light}])

    def handle_temperature(self, timestamp, temperature, humidity):
        self.pub_socket.send_multipart(['temperature', {timestamp, temperature}])
        self.pub_socket.send_multipart(['humidity', {timestamp, humidity}])

    def handle_water(self, timestamp, is_water):
        self.pub_socket.send_multipart(['water', {timestamp, is_water}])

    def handle_soil(self, timestamp, is_wet):
        self.pub_socket.send_multipart(['soil', {timestamp, is_wet}])
