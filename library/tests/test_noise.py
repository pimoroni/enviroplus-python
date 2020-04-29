import sys
import mock
import pytest


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


def test_noise_setup(sounddevice, numpy):
    force_reimport('enviroplus.noise')
    from enviroplus.noise import Noise

    noise = Noise(sample_rate=16000, duration=0.1)
    del noise


def test_noise_get_amplitudes_at_frequency_ranges(sounddevice, numpy):
    # Ippity zippidy what is this farce
    # a curious function that makes my tests pass?
    force_reimport('enviroplus.noise')
    from enviroplus.noise import Noise

    noise = Noise(sample_rate=16000, duration=0.1)
    noise.get_amplitudes_at_frequency_ranges([
        (100, 500),
        (501, 1000)
    ])

    sounddevice.rec.assert_called_with(0.1 * 16000, samplerate=16000, blocking=True, channels=1, dtype='float64')


def test_noise_get_noise_profile(sounddevice, numpy):
    # Ippity zippidy what is this farce
    # a curious function that makes my tests pass?
    force_reimport('enviroplus.noise')
    from enviroplus.noise import Noise

    noise = Noise(sample_rate=16000, duration=0.1)
    amp_low, amp_mid, amp_high, amp_total = noise.get_noise_profile(
        noise_floor=100,
        low=0.12,
        mid=0.36,
        high=None)

    sounddevice.rec.assert_called_with(0.1 * 16000, samplerate=16000, blocking=True, channels=1, dtype='float64')


def test_get_amplitude_at_frequency_range(sounddevice, numpy):
    # Ippity zippidy what is this farce
    # a curious function that makes my tests pass?
    force_reimport('enviroplus.noise')
    from enviroplus.noise import Noise

    noise = Noise(sample_rate=16000, duration=0.1)

    noise.get_amplitude_at_frequency_range(0, 8000)

    with pytest.raises(ValueError):
        noise.get_amplitude_at_frequency_range(0, 16000)
