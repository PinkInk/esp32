import ssd1306
import math


class Dial(ssd1306.SSD1306):

    def __init__(self, i2c, vmin, vmax, h=64):
        self.last = None
        self.rmin = vmin
        self.rscale = (math.pi*2)/(vmax-vmin)
        super().__init__(i2c, h)

    @staticmethod
    def rotate(x, y, cx, cy, t):
        return math.cos(t) * (x - cx) - math.sin(t) * (y - cy) + cx,\
               math.sin(t) * (x - cx) + math.cos(t) * (y - cy) + cy

    def __call__(self, value, solid=True):
        self.fill(0) # clear contents

        cx = (self.width-1)//2
        cy = (self.height-1)//2
        t = (value-self.rmin)*self.rscale

        if solid:
            x, y = map(int, self.rotate(cx, -20, cx, cy, t))
            self.fill_circle(cx, cy, cy, 1)
            self.fill_circle(cx, cy, (self.height-20)//2, 0)
            if t > math.pi * 1.5:
                self.fill_triangle(cx, cy, cx, -20, x, y, 0)
            elif t > math.pi:
                self.fill_triangle(cx, cy, 20, cy, x, y, 0)
            elif t > math.pi * 0.5:
                self.fill_triangle(cx, cy, cx, self.height+20, x, y, 0)
            else:
                self.fill_triangle(cx, cy, self.width, cy, x, y, 0)
            if t <= math.pi * 1.5:
                self.fill_triangle(cx, cy, cx, -20, 20, cy, 0)
            if t <= math.pi:
                self.fill_triangle(cx, cy, cx, self.height+20, 20, cy, 0)
            if t <= math.pi * 0.5:
                self.fill_triangle(cx, cy, self.width, cy, cx, self.height+20, 0)
        else:
            x1, y1 = map(int, self.rotate(cx, 1, cx, cy, t))
            x2, y2 = map(int, self.rotate(cx, 9, cx, cy, t))
            self.line(x1, y1, x2, y2, 1)
            self.circle(cx, cy, cy, 1)
            self.circle(cx, cy, (self.height-20)//2, 1)

        self.text(
            str(value),
            cx-((len(str(value))*8)//2),
            (self.height-1-4)//2,
        )

        self.show()
