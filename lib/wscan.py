import machine
import network
import calibril8 as font
import ssd1306
import d2
from writer import Writer

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
d = ssd1306.SSD1306(i2c)
c8 = Writer(d, font, verbose=False)
ystep = 8

SSID = 0
BSSID = 1
CHANNEL = 2
RSSI = 3
AUTHMODE = 4
HIDDEN = 5

wlan = network.WLAN(network.STA_IF)

scale = d2.scale_linear(-120, 0, d.width//2, d.width)

ssids = wlan.scan()
# max_rssi = max(map(lambda ssid: ssid[RSSI], ssids))
# min_rssi = min(map(lambda ssid: ssid[RSSI], ssids))
# scale = d2.scale_linear(min_rssi-10, max_rssi+10, d.width//2, d.width)

c8.set_textpos(0, 0)
yline = font.height() // 2 # half character height

for ssid in ssids:
    c8.printstring(str(ssid[SSID], 'utf-8') + '\n')
    xrssi = scale(ssid[RSSI])
    d.line(64, yline, xrssi, yline, 1)
    d.line(64, yline-1, 64, yline+1, 1)
    d.line(xrssi, yline-1, xrssi, yline+1, 1)
    yline += ystep

d.show()
