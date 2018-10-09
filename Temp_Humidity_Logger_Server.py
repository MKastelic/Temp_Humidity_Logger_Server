import machine
import time
import dht
from ntptime import settime
import network

d = dht.DHT22(machine.Pin(4))

html = """<!DOCTYPE html>
<html>
    <head> <title>Cooper's Dome</title> </head>
    <body> <h1>Temperature & Humidity</h1>
        <table border="1"> <tr><th>Temperature (C)</th><th>Humidity (RH)</th></tr> %s </table>
    </body>
</html>
"""

import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

    
def datalog(temp_value):
    
    (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()

    days= {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
    months = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
   
    f = open('data.txt', 'w')
    f.write(months[month] + "-" + mday + "-" + year + "   " + hour + ":" + minute, temp_value)
    f.close()
 
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('5JYD2','18013D3211')
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(1)
        settime()
        
do_connect()
settime()
(year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
start_minute = minute
d.measure()
temp = d.temperature()
max_temp = temp
min_temp = temp
while True:
    do_connect()
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    d.measure()
    temp = d.temperature()
    humid = d.humidity()
    rows = ['<tr><td>%4.1f</td><td>%4.1f</td></tr>' % (temp, humid)]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
    (year, month, mday, hour, minute, second, weekday, yearday) = utime.localtime()
    if (minute - start_minute) >= 1.0:
        start_minute = minute
        if temp > max_temp:
            max_temp = temp
        if temp < min_temp:
            min_temp = temp
        datalog(temp)
    time.sleep(2)
