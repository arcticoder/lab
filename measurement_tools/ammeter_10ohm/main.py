import machine
import time

adc = machine.ADC(26)  # GPIO 26 = ADC0
shunt_ohms = 10.0

while True:
    raw = adc.read_u16()  # 16-bit: 0–65535
    voltage = (raw / 65535.0) * 3.3  # Convert to volts
    current_ma = (voltage / shunt_ohms) * 1000
    print(f"{current_ma:.2f} mA")
    time.sleep(0.1)