import socket
import machine

html = """<!DOCTYPE html>
<html>
<head> <title>ESP8266 LED ON/OFF</title> </head>
<script language="javascript">
function sendRequest(value) {
    var request=new XMLHttpRequest();
    request.open("POST", "/", false);
    request.send("LED="+value);
}
</script>
<body>
<center><h2>Micropython - Led ON/OFF</h2></center>
Collegamenti led: <br>
- pin GND led: qualsiasi pin GND della NodeMCU; <br>
- pin +: pin D4 (GPIO2) della NodeMCU.
<br>
<br>
<br>
led on GPIO2:
<button name="LED" onclick="sendRequest('ON')" type="button">LED ON (GPIO2)</button>
<button name="LED" onclick="sendRequest('OFF')" type="button">LED OFF (GPIO2)</button>
</body></html>
"""

#Setup led: GPIO2
led = machine.Pin(2, machine.Pin.OUT)

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request_bytes = conn.recv(1024)
    print("Request content = %s" % str(request_bytes))
    request = request_bytes.decode("utf-8")
    led_on = request.find('LED=ON')
    led_off = request.find('LED=OFF')

    if led_on > 0 or led_off > 0:
        if led_on > 100:
            print('TURN LED ON')
            led.high()
        if led_off > 100:
            print('TURN LED OFF')
            led.low()
    else:
        conn.send(html)

    conn.close()
    print("Connection with %s closed" % str(addr))
