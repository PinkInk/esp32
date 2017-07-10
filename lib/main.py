import machine, ssd1306

d = ssd1306.SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))