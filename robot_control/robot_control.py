import socket
import machine

# D1: GPIO5: Motor A
p5 = machine.Pin(5)
motor_left_pin = machine.PWM(p5, freq=1000)

# D2: GPIO4: Motor B
p4 = machine.Pin(4)
motor_right_pin = machine.PWM(p4, freq=1000)

# D3: GPIO0: direction A
direction_left = machine.Pin(0, machine.Pin.OUT)
# D4: GPIO2: direction B
direction_right = machine.Pin(2, machine.Pin.OUT)


def go_forward():
    reset_motors()
    motor_left(750, 1)
    motor_right(750, 1)


def go_backward():
    reset_motors()
    motor_left(750, 0)
    motor_right(750, 0)


def go_right():
    reset_motors()
    motor_left(500, 1)
    motor_right(500, 0)


def go_left():
    reset_motors()
    motor_left(500, 0)
    motor_right(500, 1)


def motor_left(duty, motor_direction):
    if motor_direction == 1:
        direction_left.high()
    else:
        direction_left.low()
    motor_left_pin.duty(duty)


def motor_right(duty, motor_direction):
    if motor_direction == 1:
        direction_right.low()
    else:
        direction_right.high()
    motor_right_pin.duty(duty)


def reset_motors():
    motor_left_pin.duty(0)
    motor_right_pin.duty(0)

# init:
reset_motors()



# addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TODO: what?

s = socket.socket()
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request_bytes = conn.recv(1024)

    conn.sendall('HTTP/1.1 200 OK\nConnection: close\nServer: NodeMCU\nContent-Type: text/html\n\n')

    print("Request content = %s" % str(request_bytes))
    request = request_bytes.decode("utf-8")
    command_go_forward = request.find('COMMAND=FORWARD')
    command_go_backward = request.find('COMMAND=BACKWARD')
    command_go_right = request.find('COMMAND=RIGHT')
    command_go_left = request.find('COMMAND=LEFT')
    command_stop = request.find('COMMAND=STOP')
    # check image:
    request_favicon = request.find('/favicon.ico')
    request_image = request.find('/img/')

    if request_favicon > 0:
        print('favicon requested.')
        with open("/favicon.ico", "rb") as img:
            conn.sendall(img.read())
    elif request_image > 0:
        file_img = request[request_image+5:request.find('.png')] + ".png"
        print('image requested: %s' % file_img)
        with open("/img/"+file_img, "rb") as img:
            conn.send(img.read())
    elif command_go_forward > 0:
        print('go forward')
        go_forward()
    elif command_go_backward > 0:
        print('go backward')
        go_backward()
    elif command_go_right > 0:
        print('go right')
        go_right()
    elif command_go_left > 0:
        print('go left')
        go_left()
    elif command_stop > 0:
        print('stop motors')
        reset_motors()
    else:
        with open('commands.html', 'r') as html:
            conn.sendall(html.read())

    conn.sendall('\n')
    conn.close()
    print("Connection with %s closed" % str(addr))
