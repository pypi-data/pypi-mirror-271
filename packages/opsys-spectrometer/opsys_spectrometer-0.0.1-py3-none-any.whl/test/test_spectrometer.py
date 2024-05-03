import unittest
from unittest.mock import patch, MagicMock
from opsys_spectrometer.spectrometer_controller import SpectrometerController


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(SpectrometerController, 'connect')
    def test_connect(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.connect()
        spectro_mock.assert_called_once_with()

    @ patch.object(SpectrometerController, 'get_lambda')
    def test_get_lambda(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.get_lambda()
        spectro_mock.assert_called_once_with()
        
    @ patch.object(SpectrometerController, 'get_peak_value')
    def test_get_peak_value(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.get_peak_value()
        spectro_mock.assert_called_once_with()
        
    @ patch.object(SpectrometerController, 'get_fwhm')
    def test_get_fwhm(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.get_fwhm()
        spectro_mock.assert_called_once_with()
        
    @ patch.object(SpectrometerController, 'get_dll_version')
    def test_get_dll_version(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.get_dll_version()
        spectro_mock.assert_called_once_with()
        
    @ patch.object(SpectrometerController, 'measure')
    def test_measure(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.measure()
        spectro_mock.assert_called_once_with()
        
    @ patch.object(SpectrometerController, 'get_num_pixels')
    def test_get_num_pixels(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.get_num_pixels()
        spectro_mock.assert_called_once_with()
        
    @ patch.object(SpectrometerController, 'disconnect')
    def test_disconnect(self, spectro_mock: MagicMock):
        spectrometer = SpectrometerController()
        spectrometer.disconnect()
        spectro_mock.assert_called_once_with()
