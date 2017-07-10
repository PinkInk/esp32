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
from d2 import rotate

d = SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))

cx, cy = d.width//2-1, d.height//2-1
yd = 0
i = 0
di = 1
while True:
    points = []
    for a in range(0, 360, 60):
        points.append(rotate(cx, cy-i, cx, cy, math.radians(a+yd)))
    d.fill(0)
    for p1 in points:
        for p2 in points:
            d.line(p1[0], p1[1], p2[0], p2[1], 1)
    if i%2:
        d.invert()
    d.show()
    yd += 5
    i += di
    if i == 64 or i == 0:
        di = -di
# --------------------------------------------------------

import d2
from math import pi
from time import sleep
c = d.width//2-1, d.height//2-1
m = c[0], 0
for i in range(2, 10):
    points = tuple(d2.rotate(*m+c+((pi*2/i)*j,)) for j in range(i))
    d.fill(0)
    for pt in points:
        for pt1 in points:
            d.line(*pt+pt1+(1,))
    d.show()
    sleep(.1)
# --------------------------------------------------------

import d2, math
cx, cy = d.width//2-1, d.height//2-1
d1, dy = d.height//2-1, d.height//2-14
t = (cx, 0), (cx+7, 14), (cx-7, 14)
tc = cx, 14
while True:
    for i in range(0, 360, 6):
        a = (math.pi*2/360)*i
        td = tuple(
            map(
                lambda pt: d2.rotate(pt[0], pt[1], cx, cy, a),
                t
            )
        )
        tcd = d2.rotate(tc[0], tc[1], cx, cy, a)
        d.fill(0)
        d.triangle(*td[0]+td[1]+td[2]+(1,))
        d.line(cx, cy, tcd[0], tcd[1], 1)
        d.show()
# --------------------------------------------------------

import math
import machine, ssd1306
from ssd1306 import SSD1306
import d3

d = ssd1306.SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))
cx, cy = d.width//2-1, d.height//2-1
l = 20
center = cx, cy, l

# ============== MODEL: CUBE ==============
cube = (
    ( # bottom face
        (cx-l, cy-l, 0),
        (cx+l, cy-l, 0),
        (cx+l, cy+l, 0),
        (cx-l, cy+l, 0),
        (cx-l, cy-l, 0),
    ),
    ( # top face
        (cx-l, cy-l, 2*l),
        (cx+l, cy-l, 2*l),
        (cx+l, cy+l, 2*l),
        (cx-l, cy+l, 2*l),
        (cx-l, cy-l, 2*l),
    ),
    # verticals
    ((cx-l, cy-l, 0), (cx-l, cy-l, 2*l)),
    ((cx+l, cy-l, 0), (cx+l, cy-l, 2*l)),
    ((cx+l, cy+l, 0), (cx+l, cy+l, 2*l)),
    ((cx-l, cy+l, 0), (cx-l, cy+l, 2*l)),
)

dt = 0
while True:
    d.fill(0)
    # d3.renderPoly(d, cube,
    #     lambda pt: d3.rotateXYZ(pt, center, (dt, dt, dt)),
    # )
    for path in cube:
        previous = ()
        for point in path:
            point = d3.rotateXYZ(point, center, (dt, dt, dt))
            point = tuple(map(int, point))
            if previous:
                d.line(
                    point[0], point[1],
                    previous[0], previous[1],
                    1
                )
            previous = point
    d.show()
    dt += math.pi/24
