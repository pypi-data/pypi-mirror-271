from abc import ABC, abstractmethod


class SpectrometerAbstract(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def get_lambda(self):
        pass
    
    @abstractmethod
    def get_peak_value(self):
        pass
    
    @abstractmethod
    def get_fwhm(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass
    