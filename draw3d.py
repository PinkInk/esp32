import gc
import math
import machine
from ssd1306 import SSD1306
from d3 import *

d = SSD1306(machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5)))
cx, cy = d.width//2-1, d.height//2-1
l, m = 20, 3
center = cx, cy, l
repeats = 100

gc.collect()

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
point = cx, cy-l, l
for a in range(0, 360, 45):
    circle.append(rotateZ(point, center, math.radians(a)))
sphere = []
for a in range(0, 360, 45):
    for point in circle:
        sphere.append(rotateY(point, center, math.radians(a)))

# ============== MODEL: TORUS ==============
ring = []
dcen = cx+40, cy, l
dpt = cx+40, cy-15, l
for a in range(0, 361, 45):
    ring.append(rotateZ(dpt, dcen, math.radians(a)))
torus = []
for a in range(0, 360, 30):
    torus.append([])
    for pt in ring:
        torus[-1].append(rotateY(pt, center, math.radians(a)))

# ============== MODEL: CUBE ISOLATED FACES ==============
scalev = (.8, .8, .8)
cubeface = (
    ( # bottom face
        scale((cx-l, cy-l, 0), (cx, cy, l), scalev),
        scale((cx+l, cy-l, 0), (cx, cy, l), scalev),
        scale((cx+l, cy+l, 0), (cx, cy, l), scalev),
        scale((cx-l, cy+l, 0), (cx, cy, l), scalev),
        scale((cx-l, cy-l, 0), (cx, cy, l), scalev),
    ),
    ( # top face
        scale((cx-l, cy-l, 2*l), (cx, cy, 2*l), scalev),
        scale((cx+l, cy-l, 2*l), (cx, cy, 2*l), scalev),
        scale((cx+l, cy+l, 2*l), (cx, cy, 2*l), scalev),
        scale((cx-l, cy+l, 2*l), (cx, cy, 2*l), scalev),
        scale((cx-l, cy-l, 2*l), (cx, cy, 2*l), scalev),
    ),
    ( # 12 o'clock
        scale((cx-l, cy-l, 0), (cx, cy-l, l), scalev),
        scale((cx+l, cy-l, 0), (cx, cy-l, l), scalev),
        scale((cx+l, cy-l, 2*l), (cx, cy-l, l), scalev),
        scale((cx-l, cy-l, 2*l), (cx, cy-l, l), scalev),
        scale((cx-l, cy-l, 0), (cx, cy-l, l), scalev),
    ),
    ( # 3 o'clock
        scale((cx+l, cy-l, 0), (cx+l, cy, l), scalev),
        scale((cx+l, cy+l, 0), (cx+l, cy, l), scalev),
        scale((cx+l, cy+l, 2*l), (cx+l, cy, l), scalev),
        scale((cx+l, cy-l, 2*l), (cx+l, cy, l), scalev),
        scale((cx+l, cy-l, 0), (cx+l, cy, l), scalev),
    ),
    ( # 6 o'clock
        scale((cx+l, cy+l, 0), (cx+l, cy+l, l), scalev),
        scale((cx-l, cy+l, 0), (cx+l, cy+l, l), scalev),
        scale((cx-l, cy+l, 2*l), (cx+l, cy+l, l), scalev),
        scale((cx+l, cy+l, 2*l), (cx+l, cy+l, l), scalev),
        scale((cx+l, cy+l, 0), (cx+l, cy+l, l), scalev),
    ),
    ( # 9 o'clock
        scale((cx-l, cy+l, 0), (cx-l, cy+l, l), scalev),
        scale((cx-l, cy-l, 0), (cx-l, cy+l, l), scalev),
        scale((cx-l, cy-l, 2*l), (cx-l, cy+l, l), scalev),
        scale((cx-l, cy+l, 2*l), (cx-l, cy+l, l), scalev),
        scale((cx-l, cy+l, 0), (cx-l, cy+l, l), scalev),
    ),
)

# ============== MODEL: TERRAIN ==============
from random import randint
points = []
count = 7
for x in range(count):
    points.append([])
    for y in range(count):
        points[-1].append(20+randint(0, 10))
terrain = []
for x in range(count):
    terrain.append([])
    for z in range(count):
        terrain[-1].append((cx - (10*count/2) + x*10, cy/2 + points[x][z], l - (10*count/2) + z*10))
for z in range(count):
    terrain.append([])
    for x in range(count):
        terrain[-1].append((cx - (10*count/2) + x*10, cy/2 + points[x][z], l - (10*count/2) + z*10))


gc.collect()

while True:

    # ============== RENDER: CUBE ==============
    dt = 0
    for _ in range(repeats):
        d.fill(0)
        renderPoly(d, cube,
            lambda pt: rotateXYZ(pt, center, (dt, dt, dt)),
        )
        d.show()
        dt += math.pi/24

    # ============== RENDER: SPHERE ==============
    dt = 0
    for _ in range(repeats):
        d.fill(0)
        renderCloud(d, sphere,
            lambda pt: rotateXYZ(pt, center, (dt, dt, dt)),
        )
        d.show()
        dt += math.pi/24

    # ============== RENDER: TORUS ==============
    dt = 0
    for _ in range(repeats):
        d.fill(0)
        renderPoly(d, torus,
            lambda pt: rotateXYZ(pt, center, (dt, dt, 0)),
            lambda pt: weakPerspectiveZ(pt, center, 80)
        )
        d.show()
        dt += math.pi/36

    # ============== RENDER: CUBE ISOLATED FACES ==============
    dt = 0
    for _ in range(repeats):
        d.fill(0)
        renderPoly(d, cubeface,
            lambda pt: rotateXYZ(pt, center, (dt, dt, dt)),
            lambda pt: weakPerspectiveZ(pt, center, 60)
        )
        d.show()
        dt += math.pi/24

    # ============== RENDER: TERRAIN ==============
    dt = 0
    for _ in range(repeats):
        d.fill(0)
        renderPoly(d, terrain,
            lambda pt: rotateY(pt, center, dt),
            lambda pt: weakPerspectiveZ(pt, center, 100)
        )
        d.show()
        dt += math.pi/24
    
    gc.collect()

