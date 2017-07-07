# Partially from Adafruit GFX Library (https://github.com/adafruit/Adafruit-GFX-Library)

# Copyright (c) 2013 Adafruit Industries.  All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from d2 import intersection, pt_on_line


def circle(display, cx, cy, r, color):
    pixel = display.buffer.pixel
    f = 1-r
    ddF_x = 1
    ddF_y = -2 * r
    x = 0
    y = r
    pixel(cx, cy+r, color)
    pixel(cx, cy-r, color)
    pixel(cx+r, cy, color)
    pixel(cx-r, cy, color)
    while x < y:
        if f >= 0:
            y -= 1
            ddF_y += 2
            f += ddF_y
        x += 1
        ddF_x += 2
        f += ddF_x
        pixel(cx+x, cy+y, color)
        pixel(cx-x, cy+y, color)
        pixel(cx+x, cy-y, color)
        pixel(cx-x, cy-y, color)
        pixel(cx+y, cy+x, color)
        pixel(cx-y, cy+x, color)
        pixel(cx+y, cy-x, color)
        pixel(cx-y, cy-x, color)

def fill_circle(display, cx, cy, r, color):
    line = display.buffer.line
    line(cx, cy-r, cx, cy-r+2*r+1, color)
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
        line(cx+x, cy-y, cx+x, cy-y+2*y+1, color)
        line(cx+y, cy-x, cx+y, cy-x+2*x+1, color)
        line(cx-x, cy-y, cx-x, cy-y+2*y+1, color)
        line(cx-y, cy-x, cx-y, cy-x+2*x+1, color)

def triangle(display, x0, y0, x1, y1, x2, y2, color):
    line = display.buffer.line
    line(x0, y0, x1, y1, color)
    line(x1, y1, x2, y2, color)
    line(x2, y2, x0, y0, color)

def fill_triangle(display, x0, y0, x1, y1, x2, y2, color):
    hline = display.buffer.hline
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
        hline(a, y0, b+1-a, color)
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
        hline(int(a), y, int(b+1-a), color)
    sa = dx12 * (y - y1)
    sb = dx02 * (y - y0)
    for y in range(last+1, y2+1):
        a = x1 + sa / dy12
        b = x0 + sb / dy02
        sa += dx12
        sb += dx02
        if a > b:
            a, b = b, a
        hline(int(a), y, int(b+1-a), color)

def polyline(display, polyline, color, close=False):
    line = display.buffer.line
    previous = None
    for point in polyline:
        if previous:
            line(*previous+point+(color,))
        previous = point
    if close:
        line(*previous+polyline[0]+(color,))

def fill_polyline(display, polyline, color, close=False):
    hline = display.buffer.hline
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
        if close:
            intersect = intersection(ray, (previous, polyline[0]))
            if intersect \
                    and pt_on_line(ray, intersect) \
                    and pt_on_line((previous, point), intersect):
                ints.append(tuple(map(int, intersect)))
        ints = sorted(ints, key=lambda a: a[0])
        for i, pt in enumerate(ints):
            if i%2:
                hline(
                    ints[i-1][0], ints[i-1][1],
                    pt[0]-ints[i-1][0],
                    1
                )
