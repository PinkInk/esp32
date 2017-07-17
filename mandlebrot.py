import d2
import machine, ssd1306

d = ssd1306.SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))

xscale = d2.scale_linear(0, d.width, -2.5, 1, False)
yscale = d2.scale_linear(0, d.height, -1, 1, False)

imax = 10
imax1 = imax + 1
for y in range(d.height):
    y0 = yscale(y)
    for x in range(d.width):
        x0 = xscale(x)
        c = z = complex(x0, y0)
        for i in range(1, imax1):
            if abs(z) > 2:
                break
            z = z*z + c
        if i == imax:
            d.pixel(x, y, 1)

d.show()
