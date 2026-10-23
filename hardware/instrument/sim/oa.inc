* Behavioral op-amps for the instrument's analog blocks.
* oa_tlv9062: TLV9062 (TI data sheet): gain-bandwidth 10 MHz at 5 V, phase margin 55 deg at unity gain, slew rate
*   6.5 V/us, open-loop output impedance 100 ohm (resistive), rail-to-rail input and output, DC gain 103 dB.
*   (Replace with TI's SPICE macro model before layout; this one has no noise, offset or clamp dynamics beyond the rails.)
* oa_opa197: OPA197 (TI): 10 MHz, 20 V/us, rail-to-rail output.
* Pins: inp inn out vcc vee.   Open-loop pole at GBW/A0; a second pole at 3x GBW gives about the data sheet's 55-60 deg margin.
.subckt oa_tlv9062 inp inn out vcc vee
Eg  x 0 inp inn 1.4e5
Rp  x y 1k
Cp  y 0 2.23u
Rp2 y z 1k
Cp2 z 0 5.3p
Bo  o 0 V = min(max(V(z), V(vee)+0.01), V(vcc)-0.01)
Ro  o out 100
.ends

.subckt oa_opa197 inp inn out vcc vee
Eg  x 0 inp inn 1.0e7
Rp  x y 1k
Cp  y 0 1.6u
Rp2 y z 1k
Cp2 z 0 5.3p
Bo  o 0 V = min(max(V(z), V(vee)+0.025), V(vcc)-0.025)
Ro  o out 30
.ends
