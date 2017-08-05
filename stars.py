import math
import random
import machine
import ssd1306
import d2

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))

d = ssd1306.SSD1306(i2c)
w = d.width
h = d.height
cx = w//2
cy = h//2

stars = []

while True:

    stars.append([1, random.random()*math.pi*2])

    d.fill(0)
    for i, star in enumerate(stars):
        x, y = d2.rotate(cx, cy-star[0], cx, cy, star[1])

        if 0 <= x <= w and 0 <= y <= h:
            d.pixel(x, y, 1)
            stars[i][0] *= 1.1
        else:
            del stars[i]

    d.show()
