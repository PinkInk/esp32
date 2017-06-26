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

# --------------------------------------------------------
import machine, math
from ssd1306 import SSD1306

d = SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))

def rotate(x, y, cx, cy, t, flatten=False):
    if flatten:
        return int(math.cos(t) * (x - cx) - math.sin(t) * (y - cy) + cx),\
                int(math.sin(t) * (x - cx) + math.cos(t) * (y - cy) + cy)
    else:
        return math.cos(t) * (x - cx) - math.sin(t) * (y - cy) + cx,\
                math.sin(t) * (x - cx) + math.cos(t) * (y - cy) + cy

cx, cy = d.width//2-1, d.height//2-1
yd = 0
i = 0
di = 1
while True:
    points = []
    for a in range(0, 360, 60):
        points.append(rotate(cx, cy-i, cx, cy, math.radians(a+yd), True))
    d.fill(0)
    for p1 in points:
        for p2 in points:
            d.line(p1[0], p1[1], p2[0], p2[1], 1)
    d.show()
    yd += 5
    i += di
    if i == 64 or i == 0:
        di = -di
# --------------------------------------------------------