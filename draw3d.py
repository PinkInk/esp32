import math
import machine
from ssd1306 import SSD1306

d = SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))
cx, cy = d.width//2-1, d.height//2-1
l = 15
center = cx, cy, l

def raY(point, center, theta):
    pt = tuple(map(lambda j: j[0]-j[1], zip(point, center)))
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    return (
        pt[0] * cos_t - pt[2] * sin_t + center[0],
        pt[1] + center[1],
        pt[2] * cos_t + pt[0] * sin_t + center[2]
    )

def raX(point, center, theta):
    pt = tuple(map(lambda j: j[0]-j[1], zip(point, center)))
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    return (
        pt[0] + center[0],
        pt[1] * cos_t - pt[2] * sin_t + center[1],
        pt[2] * cos_t + pt[1] * sin_t + center[2]
    )

def raZ(point, center, theta):
    pt = tuple(map(lambda j: j[0]-j[1], zip(point, center)))
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    return (
        pt[0] * cos_t - pt[1] * sin_t + center[0],
        pt[1] * cos_t + pt[0] * sin_t + center[1],
        pt[2] + center[2]
    )

# ============== MODEL: CUBE ==============
cube = (
    ( # bottom face
        (cx-l, cy-l, 0),
        (cx+l, cy-l, 0),
        (cx+l, cy+l, 0),
        (cx-l, cy+l, 0),
        (cx-l, cy-l, 0),
    ),
    ( # top face
        (cx-l, cy-l, 2*l),
        (cx+l, cy-l, 2*l),
        (cx+l, cy+l, 2*l),
        (cx-l, cy+l, 2*l),
        (cx-l, cy-l, 2*l),
    ),
    # verticals
    ((cx-l, cy-l, 0), (cx-l, cy-l, 2*l)),
    ((cx+l, cy-l, 0), (cx+l, cy-l, 2*l)),
    ((cx+l, cy+l, 0), (cx+l, cy+l, 2*l)),
    ((cx-l, cy+l, 0), (cx-l, cy+l, 2*l)),
)

# ============== MODEL: SPHERE ==============
circle = []
l = cy
point = cx, cy-l, l
for a in range(0, 360, 45):
    circle.append(raZ(point, center, math.radians(a)))

sphere = []
for a in range(0, 360, 45):
    for point in circle:
        sphere.append(raY(point, center, math.radians(a)))

# ============== MODEL: TORUS ==============
ring = []
dcen = cx+40, cy, l
dpt = cx+40, cy-15, l
for a in range(0, 361, 45):
    ring.append(raZ(dpt, dcen, math.radians(a)))

torus = []
for a in range(0, 360, 30):
    torus.append([])
    for pt in ring:
        torus[-1].append(raY(pt, center, math.radians(a)))



laps = 100
while True:
# ============== DRAW: CUBE ==============
    dt = 0
    for _ in range(laps):
        d.fill(0)
        for path in cube:
            previous = ()
            for point in path:
                point = raX(point, center, dt)
                point = raY(point, center, dt)
                point = raZ(point, center, dt)
                point = tuple(map(int, point))
                if previous:
                    d.line(point[0], point[1], previous[0], previous[1], 1)
                previous = point
        d.show()
        dt += math.pi/24

    # ============== DRAW: SPHERE ==============
    dt = 0
    for _ in range(laps):
        d.fill(0)
        for point in sphere:
            point = raX(point, center, dt)
            point = raY(point, center, dt)
            point = raZ(point, center, dt)
            point = tuple(map(int, point))
            d.pixel(point[0], point[1], 1)
        d.show()
        dt += math.pi/24

    # ============== DRAW: TORUS ==============
    dt = 0
    for _ in range(laps):
        d.fill(0)
        for path in torus:
            previous = ()
            for point in path:
                point = raX(point, center, dt)
                point = raY(point, center, dt)
                # point = raZ(point, center, dt)
                point = tuple(map(int, point))
                if previous:
                    d.line(point[0], point[1], previous[0], previous[1], 1)
                previous = point
        d.show()
        dt += math.pi/36
