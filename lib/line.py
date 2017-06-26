import ssd1306


class Line(ssd1306.SSD1306):

    rmargin = 3

    def __init__(self, i2c, vmin, vmax, h=64):
        self.last = None
        self.tick = 0
        super().__init__(i2c, h)
        self.ylow = vmin
        self.yscale = self.height/(vmax-vmin)

    def __call__(self, value=None, show_value=False):
        if value is None:
            self.tick += 1
            self.scroll(-1, 0)
        else:
            y = int(self.height-((value-self.ylow)*self.yscale))
            if self.last is None:
                self.pixel(
                    self.width-self.rmargin,
                    y,
                    1
                )
            else:
                self.line(
                    self.width-self.rmargin-self.tick,
                    int(self.height-((self.last-self.ylow)*self.yscale)),
                    self.width-self.rmargin,
                    y,
                    1
                )
                if show_value:
                    ty = self.height-8 if y > self.height-8 else y
                    self.text(
                        str(value),
                        self.width-self.rmargin-len(str(value))*8,
                        ty,
                        1
                    )
            self.last = value
            self.tick = 0
            self.scroll(-1, 0)
            self.show()
