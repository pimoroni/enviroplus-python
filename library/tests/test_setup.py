import sys
import mock
from i2cdevice import MockSMBus


class SMBusFakeDevice(MockSMBus):
    def __init__(self, i2c_bus):
        MockSMBus.__init__(self, i2c_bus)
        self.regs[0x00:0x01] = 0x0f, 0x00


def test_gas_setup():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from enviroplus import gas
    gas._is_setup = False
    gas.setup()
    gas.setup()


def test_gas_read_all():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from enviroplus import gas
    gas._is_setup = False
    result = gas.read_all()

    assert type(result.oxidising) == float
    assert int(result.oxidising) == 16641

    assert type(result.reducing) == float
    assert int(result.reducing) == 16727

    assert type(result.nh3) == float
    assert int(result.nh3) == 16813

    assert "Oxidising" in str(result)


def test_gas_read_each():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from enviroplus import gas
    gas._is_setup = False

    assert int(gas.read_oxidising()) == 16641
    assert int(gas.read_reducing()) == 16727
    assert int(gas.read_nh3()) == 16813


def test_gas_read_adc():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(2.048)
    assert gas.read_adc() == 0.255


def test_gas_read_adc_default_gain():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    assert gas.read_adc() == 0.255


def test_gas_read_adc_str():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    smbus = mock.Mock()
    smbus.SMBus = SMBusFakeDevice
    sys.modules['smbus'] = smbus
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(2.048)
    assert 'ADC' in str(gas.read_all())
