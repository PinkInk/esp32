def invert(buffer):
    for i in len(buffer):
        buffer[i] = ~buffer[i]

def invert_pixel(buffer, x, y):
    index = (y>>3) * 128 + x # relies on ssd1306 width being 128
    offset = y & 0x07
    buffer[index] = buffer[index] ^ (0x01<<offset)

def invert_rect(buffer, x, y, w, h):
    x, y, x1, y1 = min(x, x+w), min(y, y+h), max(x, x+w), max(y, y+h)
    indexes = [(i>>3)*128 for i in range(y, y1, 8)]
    masks = [] if y%8 == 0 else [0]
    for i in range(y, y1):
        i = i&0x07
        if i == 0:
            masks.append(0)
        masks[-1] = masks[-1] | (0b1<<i)
    for _x in range(x, x1):
        for idx, mask in zip(indexes, masks):
            buffer[idx+_x] = buffer[idx+_x] ^ mask
