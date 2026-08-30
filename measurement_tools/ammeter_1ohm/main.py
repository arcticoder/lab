import machine
import time

adc = machine.ADC(26)  # GPIO 26 = ADC0

# Measured shunt resistance from the voltage divider test
SHUNT_OHMS = 1.005  
V_REF = 3.3

def get_current_ma(samples=20):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
        time.sleep(0.001)
    
    avg_raw = total_raw / samples
    voltage = (avg_raw / 65535.0) * V_REF
    
    # Calculate current: I = V / R
    current_a = voltage / SHUNT_OHMS
    return current_a * 1000.0  # Convert to mA

while True:
    current_ma = get_current_ma()
    
    # Ignore baseline floating noise when disconnected
    if current_ma < 2.0:
        current_ma = 0.0

    print(f"Current: {current_ma:.1f} mA")
    time.sleep(0.1)