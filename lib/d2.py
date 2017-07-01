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

def rotate(x, y, cx, cy, t, flatten=True):
    from math import sin, cos
    dx = x - cx
    dy = y - cy
    sin_t = sin(t)
    cos_t = cos(t)
    x1 = cos_t * dx - sin_t * dy + cx
    y1 = sin_t * dx + cos_t * dy + cy
    if flatten:
        return tuple(map(int, (x1, y1)))
    else:
        return x1, y1
