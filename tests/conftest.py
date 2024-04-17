"""Test configuration.
These allow the mocking of various Python modules
that might otherwise have runtime side-effects.
"""
import sys

import mock
import pytest
from i2cdevice import MockSMBus


class SMBusFakeDevice(MockSMBus):
    def __init__(self, i2c_bus):
        MockSMBus.__init__(self, i2c_bus)
        self.regs[0x00:0x01] = 0x0f, 0x00


class SMBusFakeDeviceNoTimeout(MockSMBus):
    def __init__(self, i2c_bus):
        MockSMBus.__init__(self, i2c_bus)
        self.regs[0x00:0x01] = 0x0f, 0x80


@pytest.fixture(scope="function", autouse=True)
def cleanup():
    yield None
    modules = "enviroplus", "enviroplus.noise", "enviroplus.gas", "ads1015", "i2cdevice"
    for module in modules:
        try:
            del sys.modules[module]
        except KeyError:
            pass


@pytest.fixture(scope="function", autouse=False)
def gpiod():
    sys.modules["gpiod"] = mock.Mock()
    sys.modules["gpiod.line"] = mock.Mock()
    yield sys.modules["gpiod"]
    del sys.modules["gpiod.line"]
    del sys.modules["gpiod"]


@pytest.fixture(scope="function", autouse=False)
def gpiodevice():
    gpiodevice = mock.Mock()
    gpiodevice.get_pins_for_platform.return_value = [(mock.Mock(), 0)]
    gpiodevice.get_pin.return_value = (mock.Mock(), 0)

    sys.modules["gpiodevice"] = gpiodevice
    yield gpiodevice
    del sys.modules["gpiodevice"]


@pytest.fixture(scope="function", autouse=False)
def spidev():
    """Mock spidev module."""
    spidev = mock.MagicMock()
    sys.modules["spidev"] = spidev
    yield spidev
    del sys.modules["spidev"]


@pytest.fixture(scope="function", autouse=False)
def smbus():
    """Mock smbus2 module."""
    smbus = mock.MagicMock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules["smbus2"] = smbus
    yield smbus
    del sys.modules["smbus2"]


@pytest.fixture(scope="function", autouse=False)
def smbus_notimeout():
    """Mock smbus2 module."""
    smbus = mock.MagicMock()
    smbus.SMBus = SMBusFakeDeviceNoTimeout
    sys.modules["smbus2"] = smbus
    yield smbus
    del sys.modules["smbus2"]


@pytest.fixture(scope="function", autouse=False)
def mocksmbus():
    """Mock smbus2 module."""
    smbus = mock.MagicMock()
    sys.modules["smbus2"] = smbus
    yield smbus
    del sys.modules["smbus2"]


@pytest.fixture(scope="function", autouse=False)
def atexit():
    """Mock atexit module."""
    atexit = mock.MagicMock()
    sys.modules["atexit"] = atexit
    yield atexit
    del sys.modules["atexit"]


@pytest.fixture(scope="function", autouse=False)
def sounddevice():
    """Mock sounddevice module."""
    sounddevice = mock.MagicMock()
    sys.modules["sounddevice"] = sounddevice
    yield sounddevice
    del sys.modules["sounddevice"]


@pytest.fixture(scope="function", autouse=False)
def numpy():
    """Mock numpy module."""
    numpy = mock.MagicMock()
    sys.modules["numpy"] = numpy
    yield numpy
    del sys.modules["numpy"]
