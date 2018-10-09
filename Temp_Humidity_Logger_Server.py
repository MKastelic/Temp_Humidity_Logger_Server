import machine
import time
import dht

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
     
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    d.measure()
    rows = ['<tr><td>%4.1f</td><td>%4.1f</td></tr>' % (d.temperature(), d.humidity())]
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
    time.sleep(2)
