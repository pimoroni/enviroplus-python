"""Read the MICS6814 via an ads1015 ADC"""

import atexit
import ads1015
import RPi.GPIO as GPIO

MICS6814_HEATER_PIN = 24


ads1015.I2C_ADDRESS_DEFAULT = ads1015.I2C_ADDRESS_ALTERNATE
_is_setup = False


class Mics6814Reading(object):
    __slots__ = 'oxidising', 'reducing', 'nh3'

    def __init__(self, ox, red, nh3):
        self.oxidising = ox
        self.reducing = red
        self.nh3 = nh3

    def __repr__(self):
        return """Oxidising: {:05.02f} Ohms
Reducing: {:05.02f} Ohms
NH3: {:05.02f} Ohms
""".format(self.oxidising, self.reducing, self.nh3)

    __str__ = __repr__


def setup():
    global adc, _is_setup
    if _is_setup:
        return
    _is_setup = True

    adc = ads1015.ADS1015(i2c_addr=0x49)
    adc.set_mode('single')
    adc.set_programmable_gain(6.148)
    adc.set_sample_rate(1600)

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MICS6814_HEATER_PIN, GPIO.OUT)
    GPIO.output(MICS6814_HEATER_PIN, 1)
    atexit.register(cleanup)


def cleanup():
    GPIO.output(MICS6814_HEATER_PIN, 0)


def read_all():
    """Return gas resistence for oxidising, reducing and NH3"""
    setup()
    ox = adc.get_voltage('in0/gnd')
    red = adc.get_voltage('in1/gnd')
    nh3 = adc.get_voltage('in2/gnd')

    ox = (ox * 56000) / (3.3 - ox)
    red = (red * 56000) / (3.3 - red)
    nh3 = (nh3 * 56000) / (3.3 - nh3)

    return Mics6814Reading(ox, red, nh3)


def read_oxidising():
    """Return gas resistance for oxidising gases.

    Eg chlorine, nitrous oxide
    """
    setup()
    return read_all().oxidising


def read_reducing():
    """Return gas resistance for reducing gases.

    Eg hydrogen, carbon monoxide
    """
    setup()
    return read_all().reducing


def read_nh3():
    """Return gas resistance for nh3/ammonia"""
    setup()
    return read_all().nh3
