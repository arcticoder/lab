# Spacetime Research Circuit Dependencies & Build Order

Spacetime-research-specific circuits: gravitation/field sensor interfaces,
high-voltage pulse generation, and calorimetric/energy measurement for
electrogravitics (Biefeld-Brown effect) and Woodward-effect experiments.
These build on the general-purpose foundation (PSU tiers, protection,
safety monitoring, tiers 1–4/6/9) in
[general_purpose_circuit_dependency.md](general_purpose_circuit_dependency.md)
— see the `GENERAL` node below for exactly which upstream tiers feed in.

```mermaid
graph TD
    subgraph tier5 ["Tier 5: Specialized Sensor Interfaces"]
        HALLAMP["Hall Effect Sensor Amplifier"]
        EPFIELD["Electric Field Probe Conditioner"]
        LVDTAMP["LVDT Transducer Amplifier"]
        ACCELIF["Accelerometer/Gravitation Sensor Interface"]
        CHGAMP["Charge Amplifier"]
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

    GENERAL["General-purpose foundation: PSU tiers (incl. psu_pico_rail), protection, safety monitoring, tiers 1-4/6/9 — see general_purpose_circuit_dependency.md"]

    %% Upstream foundation feeds every spacetime-specific tier
    GENERAL --> tier5
    GENERAL --> tier7
    GENERAL --> tier8

    %% Tier 5 sensor interfaces feed general-purpose tier 6 processing
    %% (lock-in amp, anti-aliasing filter — reusable beyond spacetime work)
    HALLAMP -.feeds.-> GENERAL
    EPFIELD -.feeds.-> GENERAL
    CHGAMP -.feeds.-> GENERAL

    %% Tier 7 specialized
    MIXER --> tier7
    SWEEP --> tier7
    RFPWR --> tier8

    %% Higher tiers
    HVPULSE --> tier8
    CALORIF --> tier8

    style tier5 fill:#fce4ec
    style tier7 fill:#ede7f6
    style tier8 fill:#efebe9
    style GENERAL fill:#dcedc8,stroke:#33691e,stroke-width:2px
```
