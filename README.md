# esp32
My Esp32 [MicroPython](http://micropython.org/) experiments, mostly with cheap ebay [D-duino-32](https://www.tindie.com/products/lspoplove/d-duino-32-v2arduino-and-node32-and-esp32-and-096oled/?pt=full_prod_search) clones.

| Library |  |
|---------|-------|
| d2.py | 2d point/vector manipulations |
| d3.py | 3d point/vector manipulations |
| d2primatives.py | draw 2d primitives that aren't supported by the base ssd1306.py driver e.g. filled and unfilled circles, triangles and polylines |
| fb_utils.py | invert pixel, rectange, display on ssd1306 by directly manipulating framebuffer buffer |
| ssd1306.py | modified MicroPython ssd1306 driver |
| dial.py | dial chart |
| line.py | line chart |
