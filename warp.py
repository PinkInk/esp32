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
roll = 0

while True:

    stars.append([1, random.random()*math.pi*2])

    d.fill(0)

    if random.random() < .1:
        warp = True
        newstars = []
    else:
        warp = False

    for i, star in enumerate(stars):

        x, y = d2.rotate(cx, cy-star[0], cx, cy, star[1]+roll)

        if 0 <= x <= w and 0 <= y <= h:
            d.pixel(x, y, 1)
            if warp:
                newstars.append(star)
            stars[i][0] *= 1.1
        else:
            del stars[i]

    d.show()

    if warp:
        stars += newstars

    roll += .1
