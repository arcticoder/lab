# Spacetime Research Lab Circuit Dependencies & Build Order

```mermaid
graph TD
    subgraph safety ["[SAFETY] Monitoring & Protection Circuits"]
        THERM["Thermal Monitoring with Alarm Threshold"]
        LEAKDET["AC Leakage Current Detector / Ground Fault"]
        GFCI["GFCI Trip Detection Circuit"]
        ESDMON["ESD Event Detector"]
        INSMON["Insulation Resistance Monitor"]
        ARCDECT["Arc Detection Circuit (high-voltage)"]
        OVERCUR["Overcurrent Sensor & Alert"]
        OVERVOLT["Overvoltage Monitor & Shutdown Signal"]
        TEMPCOIL["Component-Level Thermal Overload Sensor"]
        EMSTOP["Emergency Stop Circuit Status"]
        PSUHEALTH["Power Supply Health Monitor"]
        FUSESTAT["Fuse/Circuit Breaker Status Indicator"]
        RFRAD["RF Radiation Level Detector"]
        VACPRES["Vacuum Chamber Pressure Monitor"]
        SMOKDET["Smoke/Flame Detector Interface"]
    end

    subgraph psu_system ["Power Supply System (Tiered by Load)"]
        subgraph psu_ultralow ["Ultra-Low v1: 1.5V, ~100mA, &lt;0.15W (Bootstrap)"]
            PSUUL["Single AA Battery (Alkaline) — Version 1"]
            PROTUL["Polyfuse (50mA, slow-blow)"]
        end
        
        subgraph psu_low ["Low (v2 Upgrade): 3.0V, &lt;300mA, ~0.9W"]
            PSULOW["2xAA Battery Holder in Series"]
            PROTLOW["Polyfuse (500mA) + Series Schottky Diode"]
        end
        
        subgraph psu_medlow ["Medium: 5V USB + Regulator OR 12V, 1–3A, 5–36W"]
            PSUMEDLOW["USB Wall Adapter (5V 3A) OR 12V Sabrent USB-C Adapter"]
            PROTMEDLOW["Fuse (2A fast-blow) + Polyfuse (500mA backup) for 12V path"]
        end
        
        subgraph psu_medhigh ["Medium-High: 19–24V, 2–5A, 40–120W"]
            PSUMEDHIGH["MacBook 96W/140W USB-C Adapter"]
            PROTMEDHIGH["Fuse (3A) + Electronic Current Limiter (MOSFET sense)"]
        end
        
        subgraph psu_high ["High: 48V+, Variable, 100W+"]
            PSUHIGH["Industrial Supply (external, future)"]
            PROTHIGH["Dedicated Electronic Active Limiter + Arc Detection"]
        end
    end

    subgraph protection ["Circuit Breaking & Protection (Passive)"]
        FUSE["Fuse: Ceramic/Glass Tube, Alloy Wire (100mA–5A)"]
        POLYFUSE["Polyfuse/PTC: Polymer Matrix, Resettable (50mA–2A)"]
        POLYSWITCH["Polyswitch: Polymer-Based, Different Thermal Curve"]
        ACTIVELIM["Active Current Limiter: MOSFET + Sense Resistor + Controller"]
    end

    subgraph bootstrap ["Bootstrap: Minimal-Cost Validation (Build First, No Off-Shelf Gear)"]
        PASSVM["Bootstrap DC Voltmeter — Pico ADC probe (measurement_tools/fuse_test_voltmeter/), no galvanometer build needed"]
        LEDIND["LED/Relay Presence Indicator"]
        SIMPLECNT["Basic Frequency Counter (555-gated or manual)"]
        TUNINGFK["Calibrated Tuning Fork Frequency Reference"]
        AUDIOSC["Audio-Input Oscilloscope (smartphone)"]
        CRTSC["Homemade CRT Oscilloscope"]
    end

    subgraph tier1 ["Tier 1: Foundational (Simplest, Low Cost)"]
        REF["Precision Reference Voltage Generator (3.3V or 5V input)"]
        OSC["Precision Timing Oscillator (1.5–5V)"]
        SIMPGEN["Simple Function Generator (5–12V input)"]
    end

    subgraph tier2 ["Tier 2: Essential Validation & Measurement"]
        VM["Precision DC Voltmeter"]
        AM["Precision Current Shunt Ammeter"]
        FREQC["Basic Frequency Counter"]
        TIA["Transimpedance Amplifier"]
    end

    subgraph tier3 ["Tier 3: Passive Components & Bridges"]
        OHMMETER["4-Wire Kelvin Ohmmeter"]
        CAPBRIDGE["Capacitance Bridge"]
        INDBRIDGE["Inductance Bridge"]
        TEMPCOMP["Temperature Compensation Circuit"]
    end

    subgraph tier4 ["Tier 4: Core Analog Signal Processing"]
        IA["Instrumentation Amplifier"]
        DA["Differential Amplifier"]
        PHASED["Phase Detector"]
        DEMOD["Synchronous Demodulator"]
    end

    subgraph tier5 ["Tier 5: Specialized Sensor Interfaces"]
        HALLAMP["Hall Effect Sensor Amplifier"]
        EPFIELD["Electric Field Probe Conditioner"]
        LVDTAMP["LVDT Transducer Amplifier"]
        ACCELIF["Accelerometer/Gravitation Sensor Interface"]
        CHGAMP["Charge Amplifier"]
    end

    subgraph tier6 ["Tier 6: Advanced Detection & Analysis"]
        LOCKIN["Lock-In Amplifier"]
        AAF["Anti-Aliasing Filter"]
        TIMEINT["Time Interval Measurement Circuit"]
        JITTER["Jitter Measurement Circuit"]
    end

    subgraph tier7 ["Tier 7: High-Frequency & Specialized"]
        RFPWR["RF Power Measurement Circuit"]
        MIXER["Frequency Mixer"]
        SWEEP["Precision Sweep Generator"]
        HVPULSE["High-Voltage Pulse Generator"]
    end

    subgraph tier8 ["Tier 8: Energy & Complex Measurement"]
        CALORIF["Calorimetric Transducer Interface"]
        PWRFACT["AC Power Factor Analyzer"]
        ENGINT["Energy Integrator"]
        NOISEFIG["Noise Figure Measurement Circuit"]
    end

    subgraph tier9 ["Tier 9: Data Acquisition & Integration"]
        SAMHOLD["Sample-and-Hold Circuit"]
        MUX["Analog Multiplexer with Buffer"]
        ADCDRV["ADC Driver Circuit"]
        REFGEN2["Reference Distribution Circuit"]
    end

    subgraph concurrent_meas_tools ["Validation & Test Tools (Use Alongside Build)"]
        SCOPE["Real-Time Oscilloscope or Equivalent"]
        PRECBOX["Precision Decade Box"]
        LOADBANK["Resistive Load Bank"]
        NOISEGEN["Precision Noise Source"]
        TESTSIG["Calibrated Test Signal Generator"]
        THERMOAMP["Thermocouple Amplifier"]
    end

    %% PSU upgrade path
    psu_ultralow -->|upgrade to| psu_low
    
    %% PSU system feeds safety and tier 1
    psu_system --> safety
    psu_system --> tier1
    psu_system --> protection
    
    %% Protection feeds back to PSU layers
    FUSE -.required.-> psu_medlow
    FUSE -.required.-> psu_medhigh
    POLYFUSE -.required.-> psu_ultralow
    POLYFUSE -.required.-> psu_low
    POLYFUSE -.required.-> psu_medlow
    ACTIVELIM -.required.-> psu_medhigh
    ACTIVELIM -.required.-> psu_high
    POLYSWITCH -.alternative.-> psu_low
    POLYSWITCH -.alternative.-> psu_medlow
    
    %% Safety circuits depend on Tier 1 fundamentals
    REF --> safety
    
    %% Safety monitors feed into hazardous tiers
    THERM --> tier2
    SMOKDET --> tier2
    OVERCUR --> tier7
    ARCDECT --> tier7
    OVERVOLT --> tier8
    RFRAD --> tier7
    TEMPCOIL --> tier5
    LEAKDET --> tier1
    INSMON --> tier3
    
    %% Safety interlock dependencies
    EMSTOP -.protective.-> HVPULSE
    GFCI -.protective.-> tier2
    FUSESTAT -.monitoring.-> psu_medlow

    %% Bootstrap breaks circular dependencies
    LEDIND --> psu_low
    PASSVM --> REF
    PASSVM --> psu_low
    SIMPLECNT --> OSC
    TUNINGFK --> OSC
    AUDIOSC --> SIMPGEN
    AUDIOSC --> REF
    CRTSC --> psu_low
    SIMPLECNT --> SIMPGEN

    %% Tier 1 dependencies
    REF --> tier2
    OSC --> tier2
    psu_low --> tier2
    psu_medlow --> tier2
    SIMPGEN --> tier2
    
    %% Bootstrap feeds into concurrent measurement tools
    PASSVM -.alternative.-> SCOPE
    SIMPLECNT -.alternative.-> SCOPE
    AUDIOSC -.alternative.-> SCOPE
    TUNINGFK -.calibration.-> TESTSIG

    %% Tier 2 supports tier 3
    VM --> tier3
    FREQC --> tier3
    AM --> tier3

    %% Tier 3 to tier 4
    OHMMETER --> tier4
    TEMPCOMP --> tier4

    %% Tier 4 building blocks
    IA --> tier5
    DA --> tier5
    PHASED --> tier6
    DEMOD --> tier4
    TIA --> tier5

    %% Tier 5 sensor interfaces
    HALLAMP --> tier6
    EPFIELD --> tier6
    CHGAMP --> tier6

    %% Tier 6 advanced detection
    LOCKIN --> tier6
    PHASED --> LOCKIN
    OSC --> LOCKIN
    AAF --> tier8

    %% Tier 6 to 7
    TIMEINT --> tier7
    JITTER --> tier7

    %% Tier 7 specialized
    MIXER --> tier7
    OSC --> MIXER
    SWEEP --> tier7

    %% Higher tiers
    RFPWR --> tier8
    HVPULSE --> tier8
    CALORIF --> tier8

    %% Data acquisition
    AAF --> SAMHOLD
    SAMHOLD --> MUX
    MUX --> ADCDRV
    REF --> REFGEN2

    %% Concurrent measurement tools connect to build process
    SCOPE -.validation.-> tier2
    SCOPE -.validation.-> tier3
    SCOPE -.validation.-> tier4
    PRECBOX -.calibration.-> tier3
    THERMOAMP -.validation.-> tier5
    LOADBANK -.testing.-> tier7
    NOISEGEN -.testing.-> tier8
    TESTSIG -.verification.-> tier6

    style safety fill:#ffcccc,stroke:#cc0000,stroke-width:3px,color:#000
    style psu_system fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style psu_ultralow fill:#e0f2f1,stroke:#00897b,stroke-width:2px
    style psu_low fill:#a5d6a7,stroke:#2e7d32,stroke-width:2px
    style psu_medlow fill:#81c784,stroke:#2e7d32,stroke-width:2px
    style psu_medhigh fill:#66bb6a,stroke:#1b5e20,stroke-width:2px
    style psu_high fill:#4caf50
    style protection fill:#bbdefb,stroke:#1565c0,stroke-width:2px
    style bootstrap fill:#ffccbc,stroke:#e65100,stroke-width:2px
    style tier1 fill:#e1f5e1
    style tier2 fill:#e3f2fd
    style tier3 fill:#f3e5f5
    style tier4 fill:#fff3e0
    style tier5 fill:#fce4ec
    style tier6 fill:#f1f8e9
    style tier7 fill:#ede7f6
    style tier8 fill:#efebe9
    style tier9 fill:#e0f2f1
    style concurrent_meas_tools fill:#fff9c4
