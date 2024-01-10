import pytest


def test_noise_setup(sounddevice, numpy):
    from enviroplus.noise import Noise

    noise = Noise(sample_rate=16000, duration=0.1)
    del noise


def test_noise_get_amplitudes_at_frequency_ranges(sounddevice, numpy):
    from enviroplus.noise import Noise

    noise = Noise(sample_rate=16000, duration=0.1)
    noise.get_amplitudes_at_frequency_ranges([
        (100, 500),
        (501, 1000)
    ])

    sounddevice.rec.assert_called_with(0.1 * 16000, device="adau7002", samplerate=16000, blocking=True, channels=1, dtype="float64")


def test_noise_get_noise_profile(sounddevice, numpy):
    from enviroplus.noise import Noise

    numpy.mean.return_value = 10.0

    noise = Noise(sample_rate=16000, duration=0.1)
    amp_low, amp_mid, amp_high, amp_total = noise.get_noise_profile(
        noise_floor=100,
        low=0.12,
        mid=0.36,
        high=None)

    sounddevice.rec.assert_called_with(0.1 * 16000, device="adau7002", samplerate=16000, blocking=True, channels=1, dtype="float64")

    assert amp_total == 10.0


def test_get_amplitude_at_frequency_range(sounddevice, numpy):
    from enviroplus.noise import Noise

    noise = Noise(sample_rate=16000, duration=0.1)

    noise.get_amplitude_at_frequency_range(0, 8000)

    with pytest.raises(ValueError):
        noise.get_amplitude_at_frequency_range(0, 16000)
