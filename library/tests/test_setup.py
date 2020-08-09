def test_gas_setup(GPIO, smbus):
    from enviroplus import gas
    gas._is_setup = False
    gas.setup()
    gas.setup()


def test_gas_read_all(GPIO, smbus):
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


def test_gas_read_each(GPIO, smbus):
    from enviroplus import gas
    gas._is_setup = False

    assert int(gas.read_oxidising()) == 16641
    assert int(gas.read_reducing()) == 16727
    assert int(gas.read_nh3()) == 16813


def test_gas_read_adc(GPIO, smbus):
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(2.048)
    assert gas.read_adc() == 0.255


def test_gas_read_adc_default_gain(GPIO, smbus):
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(gas.MICS6814_GAIN)
    assert gas.read_adc() == 0.765


def test_gas_read_adc_str(GPIO, smbus):
    from enviroplus import gas
    gas._is_setup = False

    gas.enable_adc(True)
    gas.set_adc_gain(2.048)
    assert 'ADC' in str(gas.read_all())


def test_gas_cleanup(GPIO, smbus):
    from enviroplus import gas

    gas.cleanup()

    GPIO.output.assert_called_with(gas.MICS6814_HEATER_PIN, 0)
