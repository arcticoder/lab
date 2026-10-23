"""
pins.py — the instrument board's RP2040 pin map and USB power budget (WP1).

The firmware (WP8) and the schematic generator (WP4) both read this file. `smoke_test.py` checks that
no GPIO is used twice, that every peripheral function asked of a pin exists on that pin (the function
table below is Table 2 of the RP2040 datasheet, read 2026-10-22), and that the power budget fits USB.
"""

# GPIO function select table (RP2040 datasheet, GPIO Bank 0 functions): gpio -> {function: signal}
_ROWS = """
0 SPI0_RX UART0_TX I2C0_SDA PWM0_A
1 SPI0_CSn UART0_RX I2C0_SCL PWM0_B
2 SPI0_SCK UART0_CTS I2C1_SDA PWM1_A
3 SPI0_TX UART0_RTS I2C1_SCL PWM1_B
4 SPI0_RX UART1_TX I2C0_SDA PWM2_A
5 SPI0_CSn UART1_RX I2C0_SCL PWM2_B
6 SPI0_SCK UART1_CTS I2C1_SDA PWM3_A
7 SPI0_TX UART1_RTS I2C1_SCL PWM3_B
8 SPI1_RX UART1_TX I2C0_SDA PWM4_A
9 SPI1_CSn UART1_RX I2C0_SCL PWM4_B
10 SPI1_SCK UART1_CTS I2C1_SDA PWM5_A
11 SPI1_TX UART1_RTS I2C1_SCL PWM5_B
12 SPI1_RX UART0_TX I2C0_SDA PWM6_A
13 SPI1_CSn UART0_RX I2C0_SCL PWM6_B
14 SPI1_SCK UART0_CTS I2C1_SDA PWM7_A
15 SPI1_TX UART0_RTS I2C1_SCL PWM7_B
16 SPI0_RX UART0_TX I2C0_SDA PWM0_A
17 SPI0_CSn UART0_RX I2C0_SCL PWM0_B
18 SPI0_SCK UART0_CTS I2C1_SDA PWM1_A
19 SPI0_TX UART0_RTS I2C1_SCL PWM1_B
20 SPI0_RX UART1_TX I2C0_SDA PWM2_A
21 SPI0_CSn UART1_RX I2C0_SCL PWM2_B
22 SPI0_SCK UART1_CTS I2C1_SDA PWM3_A
23 SPI0_TX UART1_RTS I2C1_SCL PWM3_B
24 SPI1_RX UART1_TX I2C0_SDA PWM4_A
25 SPI1_CSn UART1_RX I2C0_SCL PWM4_B
26 SPI1_SCK UART1_CTS I2C1_SDA PWM5_A
27 SPI1_TX UART1_RTS I2C1_SCL PWM5_B
28 SPI1_RX UART0_TX I2C0_SDA PWM6_A
29 SPI1_CSn UART0_RX I2C0_SCL PWM6_B
"""
FUNCTIONS = {int(r.split()[0]): set(r.split()[1:]) | {"SIO", "PIO0", "PIO1"} for r in _ROWS.strip().splitlines()}
ADC_PINS = {26: "ADC0", 27: "ADC1", 28: "ADC2", 29: "ADC3"}

# name -> (gpio, function required or None for plain SIO/PIO use, note)
PINS = {
    "ADC_MISO": (16, "SPI0_RX", "ADS131A04 DOUT"),
    "ADC_CS": (17, "SPI0_CSn", "ADS131A04 CS (driven as a GPIO if the frame needs it held)"),
    "ADC_SCK": (18, "SPI0_SCK", "ADS131A04 SCLK"),
    "ADC_MOSI": (19, "SPI0_TX", "ADS131A04 DIN"),
    "ADC_DRDY": (20, None, "ADS131A04 DRDY, input"),
    "ADC_RESET": (21, None, "ADS131A04 RESET, output"),
    "I2C_SDA": (4, "I2C0_SDA", "DAC, magnetometer, temperature, accelerometer"),
    "I2C_SCL": (5, "I2C0_SCL", ""),
    "LED1_MOD": (6, "PIO0", "optical channel 1 LED gate (PIO square wave)"),
    "LED2_MOD": (7, "PIO0", "optical channel 2 LED gate"),
    "MOTOR1_PWM": (10, "PWM5_A", "coin motor 1 low-side MOSFET gate"),
    "MOTOR2_PWM": (11, "PWM5_B", "coin motor 2 low-side MOSFET gate"),
    "DUT_EN": (12, None, "device-under-test current source enable"),
    "BOOST_EN": (13, None, "24 V boost enable (plate driver)"),
    "STATUS_LED1": (14, None, ""),
    "STATUS_LED2": (15, None, ""),
    "DEBUG_TX": (0, "UART0_TX", "debug serial header"),
    "DEBUG_RX": (1, "UART0_RX", ""),
    "SPARE_A": (2, None, "spare header"),
    "SPARE_B": (3, None, "spare header"),
    "SPARE_C": (22, None, "spare header"),
    "SPARE_D": (23, None, "spare header"),
    "SPARE_E": (24, None, "spare header"),
    "SPARE_F": (25, None, "spare header"),
    "SPARE_G": (8, None, "spare header"),
    "SPARE_H": (9, None, "spare header"),
    "MON_24V": (26, None, "ADC0: +24 V rail through a divider"),
    "MON_5V": (27, None, "ADC1: USB 5 V through a divider"),
    "MON_LED": (28, None, "ADC2: LED sink current monitor"),
    "MON_SPARE": (29, None, "ADC3: spare, to a test pad"),
}

# USB power budget, mA from the 5 V rail at the connector (3.3 V loads are divided by the LDOs' efficiency of 1: linear regulators)
# value, source tag: [ds] data sheet, [assume] an estimate to be measured at bring-up
LOADS = {
    "RP2040 and flash": (30.0, "[assume] 125 MHz with PIO and DMA running"),
    "ADS131A04": (5.0, "[ds] AVDD 4 mA + IOVDD 0.8 mA, high-resolution mode"),
    "MCP4728 DAC": (1.0, "[assume]"),
    "op-amps (6 x TLV9062 halves)": (3.3, "[ds] 538 uA per package, three packages"),
    "I2C sensors (3 x TMP117, MMC5983MA, LIS2DW12)": (1.0, "[ds] 3 uA + 450 uA + under 1 mA"),
    "optical LEDs, both channels at peak": (40.0, "[design] 20 mA each, 50% duty averages half"),
    "24 V boost and plate driver, idle": (5.0, "[assume]"),
    "status LEDs": (4.0, "[design] 2 mA each"),
    "coin motor 1 at stall": (120.0, "[listing] 120 mA max stall"),
    "coin motor 2 at stall": (120.0, "[listing] 120 mA max stall"),
    "device-under-test current": (300.0, "[design] limit set by this budget"),
}
MODES = {
    "measurement": ["RP2040 and flash", "ADS131A04", "MCP4728 DAC", "op-amps (6 x TLV9062 halves)", "I2C sensors (3 x TMP117, MMC5983MA, LIS2DW12)", "optical LEDs, both channels at peak", "24 V boost and plate driver, idle", "status LEDs"],
    "lead-current run": ["RP2040 and flash", "ADS131A04", "MCP4728 DAC", "op-amps (6 x TLV9062 halves)", "I2C sensors (3 x TMP117, MMC5983MA, LIS2DW12)", "optical LEDs, both channels at peak", "24 V boost and plate driver, idle", "status LEDs", "device-under-test current"],
    "disturbance run": ["RP2040 and flash", "ADS131A04", "MCP4728 DAC", "op-amps (6 x TLV9062 halves)", "I2C sensors (3 x TMP117, MMC5983MA, LIS2DW12)", "optical LEDs, both channels at peak", "24 V boost and plate driver, idle", "status LEDs", "coin motor 1 at stall", "coin motor 2 at stall"],
}
# which rail each load hangs on: 5V (the fused USB rail), 3V3_D or 3V3_A (two LP5907 regulators, 250 mA each)
RAIL = {
    "RP2040 and flash": "3V3_D",
    "ADS131A04": "3V3_A",
    "MCP4728 DAC": "3V3_A",
    "op-amps (6 x TLV9062 halves)": "3V3_A",
    "I2C sensors (3 x TMP117, MMC5983MA, LIS2DW12)": "3V3_D",
    "optical LEDs, both channels at peak": "3V3_A",
    "24 V boost and plate driver, idle": "5V",
    "status LEDs": "3V3_D",
    "coin motor 1 at stall": "5V",  # PWM from 5 V, duty capped at 60% so the average is the motor's 3 V rating
    "coin motor 2 at stall": "5V",
    "device-under-test current": "5V",
}
MOTOR_DUTY_MAX = 0.60
LDO_MAX_MA = 250.0  # LP5907

USB_LIMIT_MA = 500.0
PTC_HOLD_MA = 750.0  # hold current of the input polyfuse chosen in WP2 (to be confirmed against its data sheet)


def rail_current(mode, rail):
    return sum(LOADS[n][0] for n in MODES[mode] if RAIL[n] == rail)


def mode_current(mode):
    return sum(LOADS[n][0] for n in MODES[mode])
