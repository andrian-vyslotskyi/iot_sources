from abc import abstractmethod, ABCMeta


class Handler:
    __metaclass__ = ABCMeta

    def __int__(self):
        pass

    @abstractmethod
    def handle_temperature(self, timestamp, temperature, humidity):
        pass

    @abstractmethod
    def handle_light(self, timestamp, is_light):
        pass


class ConsoleHandler(Handler):
    def handle_temperature(self, timestamp, temperature, humidity):
        print '{0:15f}\t{1:3d}\t{2:3d}'.format(timestamp, temperature, humidity)
        pass

    def handle_light(self, timestamp, is_light):
        print '{0:15f}\t{1}'.format(timestamp, is_light)
        pass
