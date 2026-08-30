import machine
import time

# Voltage-divider resistance meter: 3V3 -> R_REF -> GP26 (ADC0) -> R_x -> GND.
# R_x is whatever unknown resistance is wired into the divider's lower leg
# (built to measure a jumper-wire chain being used as a low-value current
# shunt for ammeter_1ohm/ — see README.md for the full circuit and math).
# Solving the divider for the unknown leg: R_x = R_REF * (V_out / (V_in - V_out))

# ADC Setup
adc = machine.ADC(26)  # GPIO 26 = ADC0

# CONFIGURATION: Set this to the exact value of your known upper resistor in Ohms
R_REF = 10.0

# Supply voltage on 3V3 pin (typically ~3.3V, measure with ADC if necessary)
V_IN = 3.3

def read_voltage(samples=50):
    # Averaging cuts down ADC noise before it gets divided into R_x below
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