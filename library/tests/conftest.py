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


@pytest.fixture(scope='function', autouse=True)
def cleanup():
    yield None
    try:
        del sys.modules['enviroplus']
    except KeyError:
        pass
    try:
        del sys.modules['enviroplus.noise']
    except KeyError:
        pass
    try:
        del sys.modules['enviroplus.gas']
    except KeyError:
        pass


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""
    GPIO = mock.MagicMock()
    # Fudge for Python < 37 (possibly earlier)
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi'].GPIO = GPIO
    sys.modules['RPi.GPIO'] = GPIO
    yield GPIO
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']


@pytest.fixture(scope='function', autouse=False)
def spidev():
    """Mock spidev module."""
    spidev = mock.MagicMock()
    sys.modules['spidev'] = spidev
    yield spidev
    del sys.modules['spidev']


@pytest.fixture(scope='function', autouse=False)
def smbus():
    """Mock smbus module."""
    smbus = mock.MagicMock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    yield smbus
    del sys.modules['smbus']


@pytest.fixture(scope='function', autouse=False)
def smbus_notimeout():
    """Mock smbus module."""
    smbus = mock.MagicMock()
    smbus.SMBus = SMBusFakeDeviceNoTimeout
    sys.modules['smbus'] = smbus
    yield smbus
    del sys.modules['smbus']


@pytest.fixture(scope='function', autouse=False)
def mocksmbus():
    """Mock smbus module."""
    smbus = mock.MagicMock()
    sys.modules['smbus'] = smbus
    yield smbus
    del sys.modules['smbus']


@pytest.fixture(scope='function', autouse=False)
def atexit():
    """Mock atexit module."""
    atexit = mock.MagicMock()
    sys.modules['atexit'] = atexit
    yield atexit
    del sys.modules['atexit']


@pytest.fixture(scope='function', autouse=False)
def sounddevice():
    """Mock sounddevice module."""
    sounddevice = mock.MagicMock()
    sys.modules['sounddevice'] = sounddevice
    yield sounddevice
    del sys.modules['sounddevice']


@pytest.fixture(scope='function', autouse=False)
def numpy():
    """Mock numpy module."""
    numpy = mock.MagicMock()
    sys.modules['numpy'] = numpy
    yield numpy
    del sys.modules['numpy']
