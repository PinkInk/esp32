import math

def rotateX(point, center, theta):
    pt = tuple(map(lambda j: j[0]-j[1], zip(point, center)))
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    return (
        pt[0] + center[0],
        pt[1] * cos_t - pt[2] * sin_t + center[1],
        pt[2] * cos_t + pt[1] * sin_t + center[2]
    )

def rotateY(point, center, theta):
    pt = tuple(map(lambda j: j[0]-j[1], zip(point, center)))
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    return (
        pt[0] * cos_t - pt[2] * sin_t + center[0],
        pt[1] + center[1],
        pt[2] * cos_t + pt[0] * sin_t + center[2]
    )

def rotateZ(point, center, theta):
    pt = tuple(map(lambda j: j[0]-j[1], zip(point, center)))
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    return (
        pt[0] * cos_t - pt[1] * sin_t + center[0],
        pt[1] * cos_t + pt[0] * sin_t + center[1],
        pt[2] + center[2]
    )

def rotateXYZ(point, center, angles):
    if angles[0]:
        point = rotateX(point, center, angles[0])
    if angles[1]:
        point = rotateY(point, center, angles[1])
    if angles[2]:
        point = rotateZ(point, center, angles[2])
    return point

def scale(point, center, scalev):
    return tuple(map(lambda j: (j[0]-j[1])*j[2]+j[1], zip(point, center, scalev)))

def move(point, vector):
    return tuple(map(lambda j: j[0]+j[1], zip(point, vector)))

# from functools import reduce
# def sumprod(vector1, vector2):
#    # http://www.euclideanspace.com/maths/algebra/vectors/angleBetween/index.htm
#     return reduce(lambda i, j: i+j, map(lambda j: j[0]*j[1], zip(vector1, vector2)))

# def crossprod(vector1, vector2):
#     # http://www.euclideanspace.com/maths/algebra/vectors/angleBetween/index.htm
#     return (
#         vector1[1] * vector2[2] - vector2[1] * vector1[2],
#         vector1[2] * vector2[0] - vector2[2] * vector1[0],
#         vector1[0] * vector2[1] - vector2[0] * vector1[1]
#     )

# def viewpoint(point, location, direction):
#     pass

def weakPerspectiveZ(point, center, fov):
    pt = tuple(map(lambda j: j[0]-j[1], zip(point, center)))
    scale = fov/(fov+pt[2])
    return (
        pt[0] * scale + center[0],
        pt[1] * scale + center[1],
        pt[2] + center[2]
    )
    
def fovClipZ(point, fov):
    return point[2] > fov

def _translate(point, transform=None, projection=None):
    if transform:
        point = transform(point)
    if projection:
        point = projection(point)
    return tuple(map(int, point))    

def renderPoly(display, poly, transform=None, projection=None, color=1):
    for path in poly:
        previous = ()
        for point in path:
            point = _translate(point, transform, projection)
            if previous:
                display.line(
                    point[0], point[1], 
                    previous[0], previous[1], 
                    color
                )
            previous = point

def renderCloud(display, cloud, transform=None, projection=None, color=1):
    for point in cloud:
            point = _translate(point, transform, projection)
            display.pixel(point[0], point[1], color)
