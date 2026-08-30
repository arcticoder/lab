import machine
import time

# ADC Setup
adc = machine.ADC(26)  # GPIO 26 = ADC0

# CONFIGURATION: Set this to the exact value of your known upper resistor in Ohms
R_REF = 10.0  

# Supply voltage on 3V3 pin (typically ~3.3V, measure with ADC if necessary)
V_IN = 3.3  

def read_voltage(samples=50):
    total_raw = 0
    for _ in range(samples):
        total_raw += adc.read_u16()
        time.sleep(0.001)
    avg_raw = total_raw / samples
    return (avg_raw / 65535.0) * V_IN

while True:
    v_out = read_voltage()
    
    # Avoid division by zero if disconnected or reading near 3.3V
    if v_out >= (V_IN - 0.01):
        print("Circuit Open: Connect R_x to GND")
    elif v_out <= 0.001:
        print("Short to GND or 0 Ohms")
    else:
        # Voltage divider equation solved for R_x
        r_x = R_REF * (v_out / (V_IN - v_out))
        print(f"Measured Voltage: {v_out:.3f} V | Measured Resistance (R_x): {r_x:.3f} Ohms")
    
    time.sleep(0.5)