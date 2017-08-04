import d2
import framebuf
import freesans20
import gc
import machine
import math
import ssd1306
import time
import ujson
import urequests
from writer import Writer

gc.collect()

exchange, stock = 'LON', 'CLLN'
step = 10 # round axes to nearest

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
d = ssd1306.SSD1306(i2c)
buf = bytearray(d.width*(d.height//2)//8)
g = framebuf.FrameBuffer(buf, d.width, d.height//2, framebuf.MVLSB)
fs20=Writer(d, freesans20, verbose=False)

gc.collect()

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
    tick = get_current(exchange, stock)

    if tick:

        ticks.append(round(float(tick['l']), 2))
        while len(ticks) > d.width:
            del ticks[0] # delete oldest ticks
        
        d.fill(0)

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

        diff, delta = 0, ''
        try:
            diff = ticks[-1] - ticks[-2]
            delta = ('+' if diff > 0 else '') + str(round(diff, 2))
        except:
            pass
        
        # direction arrow
        if diff:
            d.line(3, 6, 3, 18, 1 )
            if diff > 0:
                d.line(0, 9, 3, 6, 1)
                d.line(3, 6, 5, 9, 1)
            else: # diff < 0
                d.line(0, 15, 3, 18, 1)
                d.line(3, 18, 5, 15, 1)
        
        fs20.set_textpos(4, 8) # quirk: row,col i.e. reversal of x,y
        fs20.printstring('{}'.format(str(ticks[-1])))
        d.text(stock, d.width-len(stock)*8, 0, 1)
        ltt = tick['ltt'].split(' ')[0]
        d.text('{}'.format(ltt), d.width-len(ltt)*8, 8, 1)
        d.text('{}'.format(delta), d.width-len(delta)*8, 16, 1)

        d.show()

        gc.collect()

    runtime = time.ticks_diff(time.ticks_ms(), start)
    # print(runtime)

    time.sleep(60-runtime/1000)

