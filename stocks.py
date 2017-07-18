import d2
import framebuf
import gc
import machine
import math
import ssd1306
import time
import ujson
import urequests

gc.collect()

exchange, stock, currency = 'LON', 'CLLN', 'GBP'
step = 10

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
d = ssd1306.SSD1306(i2c)
buf = bytearray(d.width*(d.height//2)//8)
g = framebuf.FrameBuffer(buf, d.width, d.height//2, framebuf.MVLSB)

def get_current(exchange, stock):
    url = 'http://finance.google.com/finance/info?client=ig&q={}:{}'.format(exchange, stock)

    try:
        r = urequests.request('get', url)
    except:
        r = None

    if r is not None:
        if r.status_code == 200:
            d = ujson.loads(r.content[4:])[0]
        else:
            d = None
        r.close() # must cleanup
        return d


ticks = [] # max 128

while True:

    start = time.ticks_ms()

    tick = get_current('LON', 'CLLN')


    if tick:

        ticks.append(round(float(tick['l']), 2))

        d.fill(0)

        while len(ticks) > d.width:
            del ticks[0] # delete oldest ticks

        gmax = math.ceil(max(ticks)/step)*step
        gmin = math.floor(min(ticks)/step)*step
        y = d2.scale_linear(gmin, gmax, d.height//2, 0)

        g.fill(0)
        for i in range(d.width):
            # x axis
            if not i%10:
                for j in range(0, d.height//2, 4):
                    g.pixel(i, j, 1)
            # y axis
            if not i%5:
                for j in range(gmin, gmax, step//2):
                    g.pixel(i, y(j), 1)
            # plot
            try:
                previous = ticks[i+len(ticks)-d.width-1]
                current = ticks[i+len(ticks)-d.width]
                g.line(i-1, y(previous), i, y(current), 1)
            except:
                pass

        g.text(str(gmax), 0, 0, 1)
        g.text(str(gmin), 0, d.height//2-8, 1)

        d.blit(g, 0, d.height//2, 0)

        delta = ''
        try:
            diff = ticks[-1]-ticks[-2]
            dsign = '+' if diff > 0 else ''
            delta = dsign + str(round(diff, 2))
        except:
            pass

        d.text('{} {} {}'.format(str(ticks[-1]), currency, delta), 0, 0, 1)
        d.text('{}:{}'.format(exchange, stock), 0, 8, 1)
        d.text('{}'.format(tick['ltt']), 0, 16, 1)

        d.show()

        gc.collect()

    runtime = time.ticks_diff(time.ticks_ms(), start)
    # print(runtime)

    time.sleep(60-runtime/1000)

