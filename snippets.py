# --------------------------------------------------------
# Use fonts
import machine, ssd1306
from fonts.mono6x8 import mono6x8 as font
# from fonts.mono4x6 import mono4x6 as font
i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
d = ssd1306.SSD1306(i2c)

d.fill(0)
s = 'Hello World'
x = 0
for c in s:
  bits = font.getbitmap_str(ord(c))
  for idx, bit in enumerate(bits):
    d.pixel(x+(idx%font.w), idx//font.h, int(bit))
  x += font.w
d.show()
# --------------------------------------------------------

# --------------------------------------------------------
# big fonts
import machine, ssd1306
from fonts.mono6x8 import mono6x8 as font
# from fonts.mono4x6 import mono4x6 as font
i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
d = ssd1306.SSD1306(i2c)

d.fill(0)
s = 'Tim'
x0, y0 = 0, 0
size = 5
for c in s:
    bits = font.getbitmap_str(ord(c))
    for idx, bit in enumerate(bits):
        if int(bit):
            x, y = x0+(idx%font.w), y0+(idx//font.h)
            d.rect(
                x0+(x*size), y0+(y*size),
                size, size,
                1
            )
    x0 += font.w-1
d.show()
# --------------------------------------------------------
