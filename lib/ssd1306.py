# MicroPython SSD1306 OLED driver, I2C interface

import framebuf

# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xa4)
SET_NORM_INV = const(0xa6)
SET_DISP = const(0xae)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xa0)
SET_MUX_RATIO = const(0xa8)
SET_COM_OUT_DIR = const(0xc0)
SET_DISP_OFFSET = const(0xd3)
SET_COM_PIN_CFG = const(0xda)
SET_DISP_CLK_DIV = const(0xd5)
SET_PRECHARGE = const(0xd9)
SET_VCOM_DESEL = const(0xdb)
SET_CHARGE_PUMP = const(0x8d)

def intersection(line1, line2):
    xd = line1[0][0] - line1[1][0], line2[0][0] - line2[1][0]
    yd = line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]
    det = lambda a, b: a[0] * b[1] - a[1] * b[0]
    div = det(xd, yd)
    if div == 0:
        return False
    d = (det(*line1), det(*line2))
    x = det(d, xd) / div
    y = det(d, yd) / div
    return x, y

def pt_on_line(l, pt):
    (x1, y1), (x2, y2) = l
    return min(x1, x2) <= pt[0] <= max(x1, x2) \
        and min(y1, y2) <= pt[1] <= max(y1, y2)

def scale_linear(smin, smax, tmin, tmax, flatten=True):
    scale = (tmax - tmin) / (smax - smin)
    def close(val):
        if flatten:
            return int(((val - smin) * scale) + tmin)
        else:
            return ((val - smin) * scale) + tmin
    return close


class SSD1306:

    def __init__(self, i2c, height=64, addr=0x3c, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.width = 128
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        self.framebuf = framebuf.FrameBuffer1(self.buffer, self.width, self.height)
        self.poweron()
        self.init_display()

    def init_display(self):
        for cmd in (
                SET_DISP | 0x00, # off
                # address setting
                SET_MEM_ADDR, 0x00, # horizontal
                # resolution and layout
                SET_DISP_START_LINE | 0x00,
                SET_SEG_REMAP | 0x01, # column addr 127 mapped to SEG0
                SET_MUX_RATIO, self.height - 1,
                SET_COM_OUT_DIR | 0x08, # scan from COM[N] to COM0
                SET_DISP_OFFSET, 0x00,
                SET_COM_PIN_CFG, 0x02 if self.height == 32 else 0x12,
                # timing and driving scheme
                SET_DISP_CLK_DIV, 0x80,
                SET_PRECHARGE, 0x22 if self.external_vcc else 0xf1,
                SET_VCOM_DESEL, 0x30, # 0.83*Vcc
                # display
                SET_CONTRAST, 0xff, # maximum
                SET_ENTIRE_ON, # output follows RAM contents
                SET_NORM_INV, # not inverted
                # charge pump
                SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,
                SET_DISP | 0x01): # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def write_cmd(self, cmd):
        self.temp[0] = 0x80 # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.temp[0] = self.addr << 1
        self.temp[1] = 0x40 # Co=0, D/C#=1
        self.i2c.start()
        self.i2c.write(self.temp)
        self.i2c.write(buf)
        self.i2c.stop()

    def poweron(self):
        pass

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.width - 1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

    def fill(self, color):
        self.framebuf.fill(color)

    def pixel(self, x, y, color):
        self.framebuf.pixel(x, y, color)

    def hline(self, x, y, w, color):
        self.framebuf.hline(x, y, w, color)

    def vline(self, x, y, h, color):
        self.framebuf.vline(x, y, h, color)

    def line(self, x1, y1, x2, y2, color):
        self.framebuf.line(x1, y1, x2, y2, color)

    def rect(self, x, y, w, h, color):
        self.framebuf.rect(x, y, w, h, color)

    def fill_rect(self, x, y, w, h, color):
        self.framebuf.fill_rect(x, y, w, h, color)

    def scroll(self, dx, dy):
        self.framebuf.scroll(dx, dy)

    def text(self, string, x, y, color):
        self.framebuf.text(string, x, y, color)

    def blit(self, fbuf, x, y, key=False):
        self.framebuf.blit(fbuf, x, y, key)

    def circle(self, cx, cy, r, color):
        f = 1-r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        self.pixel(cx, cy+r, color)
        self.pixel(cx, cy-r, color)
        self.pixel(cx+r, cy, color)
        self.pixel(cx-r, cy, color)
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.pixel(cx+x, cy+y, color)
            self.pixel(cx-x, cy+y, color)
            self.pixel(cx+x, cy-y, color)
            self.pixel(cx-x, cy-y, color)
            self.pixel(cx+y, cy+x, color)
            self.pixel(cx-y, cy+x, color)
            self.pixel(cx+y, cy-x, color)
            self.pixel(cx-y, cy-x, color)

    def fill_circle(self, cx, cy, r, color):
        self.line(cx, cy-r, cx, cy-r+2*r+1, color)
        f = 1 - r
        ddF_x = 1
        ddF_y = -2 * r
        x = 0
        y = r
        while x < y:
            if f >= 0:
                y -= 1
                ddF_y += 2
                f += ddF_y
            x += 1
            ddF_x += 2
            f += ddF_x
            self.line(cx+x, cy-y, cx+x, cy-y+2*y+1, color)
            self.line(cx+y, cy-x, cx+y, cy-x+2*x+1, color)
            self.line(cx-x, cy-y, cx-x, cy-y+2*y+1, color)
            self.line(cx-y, cy-x, cx-y, cy-x+2*x+1, color)

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        self.line(x0, y0, x1, y1, color)
        self.line(x1, y1, x2, y2, color)
        self.line(x2, y2, x0, y0, color)

    def fill_triangle(self, x0, y0, x1, y1, x2, y2, color):
        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0
        if y1 > y2:
            y2, y1 = y1, y2
            x2, x1 = x1, x2
        if y0 > y1:
            y0, y1 = y1, y0
            x0, x1 = x1, x0
        if y0 == y2:
            a = x0
            b = x0
            if x1 < a:
                a = x1
            else:
                if x1 > b:
                    b = x1
            if x2 < a:
                a = x2
            else:
                if x2 > b:
                    b = x2
            self.hline(a, y0, b+1-a, color)
            return
        dx01 = x1 - x0
        dy01 = y1 - y0
        dx02 = x2 - x0
        dy02 = y2 - y0
        dx12 = x2 - x1
        dy12 = y2 - y1
        sa = 0
        sb = 0
        if y1 == y2:
            last = y1
        else:
            last = y1-1
        y = y0
        for y in range(y0, last+1):
            a = x0 + sa / dy01
            b = x0 + sb / dy02
            sa += dx01
            sb += dx02
            if a > b:
                a, b = b, a
            self.hline(int(a), y, int(b+1-a), color)
        sa = dx12 * (y - y1)
        sb = dx02 * (y - y0)
        for y in range(last+1, y2+1):
            a = x1 + sa / dy12
            b = x0 + sb / dy02
            sa += dx12
            sb += dx02
            if a > b:
                a, b = b, a
            self.hline(int(a), y, int(b+1-a), color)

    def polyline(self, polyline, color):
        previous = None
        for point in polyline:
            if previous:
                self.line(*previous+point+(color,))
            previous = point


    def fill_polyline(self, polyline, color):
        xs = tuple(map(lambda pt: pt[0], polyline))
        ys = tuple(map(lambda pt: pt[1], polyline))
        bounds = ((min(xs), min(ys)), (max(xs), max(ys)))
        for y in range(bounds[1][1]-bounds[0][1]):
            ints = []
            previous = None
            ray = (
                (bounds[0][0], y+bounds[0][1]),
                (bounds[1][0], y+bounds[0][1])
            )
            for point in polyline:
                if previous:
                    intersect = intersection(ray, (previous, point))
                    if intersect \
                            and pt_on_line(ray, intersect) \
                            and pt_on_line((previous, point), intersect):
                        ints.append(tuple(map(int, intersect)))
                previous = point
            ints = sorted(ints, key=lambda a: a[0])
            for i, pt in enumerate(ints):
                if i%2:
                    self.hline(
                        ints[i-1][0], ints[i-1][1],
                        pt[0]-ints[i-1][0],
                        1
                    )
