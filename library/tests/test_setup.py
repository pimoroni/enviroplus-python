import sys
import mock


def force_reimport(module):
    """Force the module under test to be re-imported.

    Because pytest runs all tests within the same scope (this makes me cry)
    we have to do some manual housekeeping to avoid tests polluting each other.

    Since conftest.py already does some sys.modules mangling I see no reason not to
    do the same thing here.
    """
    if "." in module:
        steps = module.split(".")
    else:
        steps = [module]
    
    for i in range(len(steps)):
        module = ".".join(steps[0:i + 1])
        try:
            del sys.modules[module]
        except KeyError:
            pass


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
    force_reimport('enviroplus.gas')
    from enviroplus import gas

    gas.cleanup()

    GPIO.output.assert_called_with(gas.MICS6814_HEATER_PIN, 0)
