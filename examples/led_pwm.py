import machine
import math
import time

p12 = machine.Pin(5)
pwm12 = machine.PWM(p12, freq=1000)

while True:
    for i in range(20):
        pwm12.duty(int(math.sin(i / 10 * math.pi) * 500 + 500))
        time.sleep_ms(50)
