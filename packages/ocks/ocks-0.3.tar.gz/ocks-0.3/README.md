# SSD1306 Library

This repository contains a modified version of the [micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306/tree/master?tab=readme-ov-file) library with the main objective of simplifying the installation process. This project has removed support for SPI and retains only the I2C functionality from the original library. All credits and acknowledgments go to the original author.

The focus of this repository is to prepare the library for uploading to PyPI and renaming it before the upload.

Test for the DUALMCU board:

```python
import machine

i2c = machine.I2C(0, sda=machine.Pin(21), scl=machine.Pin(22))

print(i2c.scan())
```
![thonny install](https://raw.githubusercontent.com/Cesarbautista10/ISE_SSD1306/main/Images/ins.png)

Code example

```py


'''
    Unit Electronics 2023
           (o_
    (o_    //\
    (/)_   V_/_ 
    tested code mark
    version: 0.0.1
    revision: 0.0.1

'''

import machine
from ocks import SSD1306_I2C

i2c = machine.I2C(0,sda=machine.Pin(21), scl=machine.Pin(22))

oled = SSD1306_I2C(128, 32, i2c)

oled.fill(1)
oled.show()

oled.fill(0)
oled.show()
oled.text('UNIT', 50, 10)
oled.text('ELECTRONICS', 25, 20)

oled.show()
```