from .spectrometer_abstract import SpectrometerAbstract
from msl.equipment import (
    EquipmentRecord,
    ConnectionRecord,
    Backend
)
import time
import numpy as np


class SpectrometerController(SpectrometerAbstract):
    """
    Wavelength measurement device interface
    """
    _scan_delay = 0.01

    def __init__(self,
                 manufacturer=None,
                 model=None,
                 serial_number=None
                 ):
        """
        constructor
        """
        self.manufacturer_name = manufacturer
        self.model = model
        self.serial_number = serial_number

    def connect(self):
        """
        Connect to device
        """
        backend_connection = ConnectionRecord(
                                address='SDK::avaspecx64.dll',
                                backend=Backend.MSL,
                                )
        self._device_interface = EquipmentRecord(
                                 manufacturer=self.manufacturer_name,
                                 model=self.model,
                                 serial=self.serial_number,
                                 connection=backend_connection
                                )
        self._spectrometer = self._device_interface.connect()
        print(f'Connected to device! DLL Version: {self.get_dll_version()}')
    
    def get_lambda(self):
        """
        Returns the wavelength values corresponding
        to the pixels if available

        Returns:
            numpy.array: wavelengths value
        """
        return self._spectrometer.get_lambda()
    
    def get_peak_value(self):
        """
        Get max measured value

        Returns:
            float: max measured value
        """
        return max(self.data)
    
    def get_fwhm(self):
        """
        Get Full Width at Half Max value,
        for given x and y values

        Returns:
            float: calculated width value
        """
        # get wavelengths (x-axis values)
        x = self.get_lambda()
        y = self.data
        
        difference = max(y) - min(y)
        HM = difference / 2
        pos_extremum = y.argmax()

        nearest_above = (np.abs(y[pos_extremum:-1] - HM)).argmin()
        nearest_below = (np.abs(y[0:pos_extremum] - HM)).argmin()

        width = (np.mean(x[nearest_above + pos_extremum]) - 
                 np.mean(x[nearest_below]))

        return width
    
    def get_dll_version(self):
        """
        Get DLL/SDK version

        Returns:
            str: DLL/SDK version
        """
        return self._spectrometer.get_dll_version()
    
    def get_parameter(self):
        """
        Get parameter - option to expand

        Returns:
            object: parameters struct
        """
        return self._spectrometer.get_parameter()
    
    def _prepare_measure(self):
        """
        Set configurations before starting
        measurement process
        """
        cfg = self._spectrometer.MeasConfigType()
        cfg.m_StopPixel = self.get_num_pixels() - 1
        cfg.m_IntegrationTime = 5  # in milliseconds
        cfg.m_NrAverages = 1  # number of averages
        self._spectrometer.prepare_measure(cfg)
    
    def measure(self, num_of_samples=-1):
        """
        Starts measurement on the spectrometer.
        If num_of_samples=-1, the measurement is
        continuous

        Args:
            num_of_samples (int, optional): Number of samples.
                                            Defaults to -1.

        Returns:
            float: pixel count and pixel value
        """
        self._prepare_measure()
        self._spectrometer.measure(num_of_samples)
        
        while not self._spectrometer.poll_scan():
            time.sleep(self._scan_delay)

        self.tick_count, self.data = self._spectrometer.get_data()
        
        return self.tick_count, self.data
    
    def get_num_pixels(self):
        """
        Returns the number of pixels of a spectrometer
        """
        return self._spectrometer.get_num_pixels()
    
    def disconnect(self):
        """
        Disconnect from the spectrometer
        """
        self._spectrometer.disconnect()
