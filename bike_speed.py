import machine
import time
import ssd1306

LAST = time.ticks_ms()
TIME = 0
FLAG = False

# hall-effect sensor
p16 = machine.Pin(16, machine.Pin.IN)

# power for the hall-effect sensor
p5 = machine.Pin(5, machine.Pin.OUT)
p5(True)

def tick(state):
    global LAST, TIME, FLAG
    now = time.ticks_ms()
    if now-LAST > 250:
        TIME = time.ticks_diff(now, LAST)
        LAST = now
        FLAG = True
        print('Now!', LAST, TIME, FLAG)
    # toggle power to the sensor
    # to toggle latch state
    p5(False)
    p5(True)

# configure
p16.irq(tick, machine.Pin.IRQ_RISING)

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
d = ssd1306.SSD1306(i2c)

while True:
    print(FLAG)
    if FLAG:
        d.fill(0)
        d.text(str(TIME), 0, 0, 1)
        d.show()
        FLAG = False
