from abc import ABCMeta, abstractmethod


class Config:
    __metaclass__ = ABCMeta

    def __int__(self):
        pass

    @abstractmethod
    def temperature_pin(self):
        pass

    @abstractmethod
    def light_pin(self):
        pass

    @abstractmethod
    def rain_pin(self):
        pass

    @abstractmethod
    def moisture_pin(self):
        pass

class DummyConfig(Config):
    def temperature_pin(self):
        return 13

    def light_pin(self):
        return 15

    def rain_pin(self):
        return 11

    def moisture_pin(self):
        pass

#TODO: add properties, distributed configs