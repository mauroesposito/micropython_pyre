import machine
import math
import time

# D1: GPIO5: Motor A
p5 = machine.Pin(5)
motor_left = machine.PWM(p5, freq=1000)

# D2: GPIO4: Motor B
p4 = machine.Pin(4)
motor_right = machine.PWM(p4, freq=1000)

# D3: GPIO0: direction A
enA = machine.Pin(0, machine.Pin.OUT)
# D4: GPIO2: direction B
enB = machine.Pin(2, machine.Pin.OUT)

enA.high()

while True:
    for i in range(20):
        motor_left.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        motor_right.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        time.sleep_ms(100)



