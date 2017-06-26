import framebuf


class LineChart():

    bpp = {
        framebuf.MVLSB: 1,
        framebuf.RGB565: 16,
        framebuf.GS4_HMSB: 4
    }

    def __init__(self, width, height, format, background=0, foreground=1):
        self.width = width
        self.height = height
        self.background = background
        self.foreground = foreground
        self.buf = bytearray(width*height*self.bpp[format]//8)
        self.fb = framebuf.FrameBuffer(self.buf, width, height, format)
        self.cbuf = bytearray((width-10)*(height-10)*self.Bpp[format]//8)
        self.cfb = framebuf.FrameBuffer(self.cbuf, width-10, height-10, format)
        self.xscale = 1
        self.yscale = 1
        self.fb.fill(background)

    def xaxis(self, min, max):
        self.xscale = self.width/max-min
        self.fb.hline(10, self.height-10, self.width, self.foreground)
        self.fb.text(str(min), 10, self.height-8, self.foreground)
        self.fb.text(str(max), self.width-(len(str(max))*8), self.height-8, self.foreground)

    def yaxis(self, min, max):
        self.yscale = self.height/max-min
        self.fb.vline(10, 0, self.height-10, self.foreground)




import machine
import ssd1306
i2c = machine.I2C(scl=machine.Pin(4),sda=machine.Pin(5))
w, h = 132, 64
d = ssd1306.SSD1306_I2C(h, i2c)
d.poweron()
d.contrast(0xff)
d.fill(0)
d.show()
a = LineChart(128,64,framebuf.MVLSB)
a.xaxis(0,100)
a.yaxis(0,10)
d.blit(a.fb,0,0)
d.show()


