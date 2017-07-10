import framebuf
import math
import time
import machine, ssd1306

d = ssd1306.SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))
plasma = bytearray(d.width*d.height)

# start = time.ticks_ms()
for x in range(d.width):
    dx2 = x-d.width/2
    for y in range(d.height):
        dy2 = y-d.height/2
        # ------------------------------------
        # i = int(math.sin((x+y)/8)*128+128)
        # ------------------------------------
        # i = int(math.sin((math.sqrt(dx2 * dx2 + dy2 * dy2))/4)*128+128)
        # ------------------------------------
        # i = int(((math.sin(x/4)*128+128) + (math.sin(y/4)*128+128))/2)
        # ------------------------------------
        i = math.sin(x/8)*128+128 \
            + math.sin(y/4)*128+128 \
            + math.sin((x+y)/8)*128+128 \
            + math.sin(math.sqrt((x**2 + y**2)*2)/4)*128+128
        i = int(i/4)
        plasma[y*d.width+x] = i

# print(time.ticks_diff(time.ticks_ms(), start))

while True:
    for i in range(0, 0xff, 10):
        d.fill(0)
        istep = i + 20 # selection width
        for y in range(d.height):
            yw = y << 7 # fast version
            for x in range(d.width):
                if i <= plasma[yw+x] < istep:
                    d.pixel(x, y, 1)
        d.show()

