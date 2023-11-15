import pytest


def test_gas_setup(gpiod, gpiodevice, smbus):
    from enviroplus import gas
    gas._is_setup = False
    gas.setup()
    gas.setup()


def test_gas_unavailable(gpiod, gpiodevice, mocksmbus):
    from enviroplus import gas
    mocksmbus.SMBus(1).read_i2c_block_data.side_effect = IOError("Oh no!")
    gas._is_setup = False
    assert gas.available() is False

    with pytest.raises(RuntimeError):
        gas.read_all()


def test_gas_available(gpiod, gpiodevice, smbus_notimeout):
    from enviroplus import gas
    gas._is_setup = False
    assert gas.available() is True


def test_gas_read_all(gpiod, gpiodevice, smbus):
    from enviroplus import gas
    gas._is_setup = False
    result = gas.read_all()

    assert isinstance(result.oxidising, float)
    assert int(result.oxidising) == 16641

    assert isinstance(result.reducing, float)
    assert int(result.reducing) == 16727

    assert isinstance(result.nh3, float)
    assert int(result.nh3) == 16813

    assert "Oxidising" in str(result)


def test_gas_read_each(gpiod, gpiodevice, smbus):
    from enviroplus import gas
    gas._is_setup = False

    assert int(gas.read_oxidising()) == 16641
    assert int(gas.read_reducing()) == 16727
    assert int(gas.read_nh3()) == 16813


def test_gas_read_adc(gpiod, gpiodevice, smbus):
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(2.048)
    assert gas.read_adc() == 0.255


def test_gas_read_adc_default_gain(gpiod, gpiodevice, smbus):
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(gas.MICS6814_GAIN)
    assert gas.read_adc() == 0.765


def test_gas_read_adc_str(gpiod, gpiodevice, smbus):
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(2.048)
    assert "ADC" in str(gas.read_all())


def test_gas_cleanup(gpiod, gpiodevice, smbus):
    from enviroplus import gas

    gas.cleanup()

    gas.setup()
    gas.cleanup()
