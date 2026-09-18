2.0.0
-----

* Enhancement: Repackage to the uv/hatchling method, with PyPI trusted publishing
* Enhancement: Version is derived from the git tag, __version__ from package metadata
* Python 3.9 or later, 3.7 and 3.8 support dropped

1.0.2
-----

* README.md: Update install instructions
* Fix installer to enable serial
* Fix gas sensor heater pin

1.0.1
-----

* README.md: Fix images

1.0.0
-----

* BREAKING: Port to gpiod/gpiodevice for Pi 5/Bookworm.

0.0.6
-----

* Fix noise by specifying adau7002 device

0.0.5
-----

* Drop Python 2.x support
* Add "available()" method for gas sensor

0.0.4
-----

* Add support for ads1015 >= v0.0.7 (ADS1115 ADCs)
* Packaging tweaks

0.0.3
-----

* Fix "self.noise_floor" bug in get_noise_profile

0.0.2
-----

* Add support for extra ADC channel in Gas
* Handle breaking change in new ltr559 library
* Add Noise functionality

0.0.1
-----

* Initial Release
