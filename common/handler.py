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

    @abstractmethod
    def handle_water(self, timestamp, is_water):
        pass

    @abstractmethod
    def handle_soil(self, timestamp, is_wet):
        pass


class ConsoleHandler(Handler):
    def handle_temperature(self, timestamp, temperature, humidity):
        print 'Temperature: {0:15f}\t{1:3d}C'.format(timestamp, temperature)
        print 'Humidity: {0:15f}\t{1:3d}%'.format(timestamp, humidity)
        pass

    def handle_light(self, timestamp, is_light):
        print 'Light: {0:15f}\t{1}'.format(timestamp, is_light)
        pass

    def handle_water(self, timestamp, is_water):
        print 'Water: {0:15f}\t{1}'.format(timestamp, is_water)
        pass

    def handle_soil(self, timestamp, is_wet):
        print 'Wet: {0:15f}\t{1}'.format(timestamp, is_wet)
        pass
