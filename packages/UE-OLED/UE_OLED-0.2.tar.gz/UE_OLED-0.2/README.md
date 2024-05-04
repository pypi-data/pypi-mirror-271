# SSD1306 Library

This repository contains a modified version of the [micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306/tree/master?tab=readme-ov-file) library with the main objective of simplifying the installation process. This project has removed support for SPI and retains only the I2C functionality from the original library. All credits and acknowledgments go to the original author.

The focus of this repository is to prepare the library for uploading to PyPI and renaming it before the upload.

Test for the DUALMCU board:

```python
import machine

i2c = machine.I2C(0, sda=machine.Pin(21), scl=machine.Pin(22))

print(i2c.scan())
```
