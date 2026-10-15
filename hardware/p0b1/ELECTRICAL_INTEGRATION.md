# P0-B1 electrical integration and terminal contract

**REVIEW; this is not a released mains, OEM connector or safety wiring drawing.**
The mechanical kit cannot be powered from this document alone. H02/H09 require an
OEM-approved terminal drawing and independent stop circuit from the integrator.
No wire colours or invented connector pins here are substitutes for that drawing.

## Selected architecture

LINAK24V LA40PL + CBJ2 + BAJ + CHJ2 + matched HB70 pendant/cables as one reviewed
kit. Keep OEM protections and motor wiring intact. A separately isolated auxiliary
24V supply powers the monitored Pilz751103 relay and field sensors; a certified
protected isolated5V branch powers the DevKit. Charger disconnected during motion.
Field24V never enters GPIO. Do not interrupt or replace OEM motor leads: the
specified actuator's shorting/self-lock arrangements must remain effective.

The integrator must draw and prove the following contact logic:

```
Dual NC E-STOP + dual-contact cell gate + approved monitored interlocks
      -> monitored manual-reset safety relay -> two independent OEM stop contacts
GPIO4 isolated request -> HW NC upper limit -> interlocked UP command contact
GPIO5 isolated request -> HW NC lower limit -> interlocked DOWN command contact
GPIO6 additional request permit -> OEM approved command enable
GPIO2 loop-alive -> external TPS3431EVM -> latched independent stop path
GPIO38 motion-only heartbeat -> commissioning monitor (NOT watchdog WDI)
```

UP and DOWN contact paths must be mutually exclusive by hardware, including a
stuck output. Safety relay reset must require a deliberate local action and
released direction commands; restoration of a gate, power or watchdog signal must
not restart a held command. A latched watchdog fault cannot clear itself as WDO
releases. A forced/welded command contact must still stop through a separate OEM
approved stop path. Confirm fault response for each single contact/driver failure.
This design has no claimed PL/SIL; fitting a certified relay does not confer one.

## Watchdog implementation detail

TI TPS3431EVM, not a software timer or Arduino reset line. Wire the EVM according
to its current user guide: EN held HIGH independently of MCU, SET1 HIGH and CWD
10kohm to VDD for preset200ms (datasheet170..230ms), supplied at3.3V. Verify actual
EVM resistor/jumper options before modification. WDO is open drain and must drive
a suitable isolated/latching interface; it cannot drive a24V relay coil directly.
At9.3mm/s,230ms accounts for2.14mm travel BEFORE relay/OEM/braking delay. Measure
total stopping movement; do not accept that calculation as a stop distance.

New GPIO2 toggles once at the END of each main loop during idle, software fault
and motion. It only proves loop progress. It is deliberately separate from GPIO38,
which stops on every motion stop. Using38 as an always-on watchdog input creates
an idle/reset deadlock. Do not generate2 from a timer interrupt that can continue
while supervision is hung. Cut/short/stick both heartbeat levels in physical tests.
The MCU liveness signal never grants motion or defeats the independent safety chain.
The interface must also supervise logic/EVM supply loss: unpowered open-drain WDO
can float HIGH. A missing3.3V supply must drop permission independently; verify this
fault with the24V field supply still present.

## Low-voltage logical terminal schedule

This is the interface contract, not a vendor connector pinout. Each24V status needs
its own reviewed isolated3.3V interface. Inputs fail LOW using external10kohm
pulldowns; all motion outputs also need external pulldowns. Maintain galvanic
isolation boundaries; no unspecified common-ground strap. Document USB isolation.

| Logical terminal | MCU GPIO | Connection and default |
| --- | ---: | --- |
| PWR5 / GNDlogic | 5V / GND | protected isolated logic supply; actual board5V pin verify |
| POS+ / POS- / POSW | conditioned3V3 / GND /1 | Gefran5kohm with1kohm end resistors and MCP6002 buffer below; calibrate |
| WD-LIVE | 2 | TPS3431 WDI,3.3V, independent liveness only |
| REQ-UP / REQ-DOWN / REQ-PERMIT | 4/5/6 | isolated OEM contacts; all LOW off |
| TOP-CLEAR / BOTTOM-CLEAR | 7/8 | isolated directional limit feedback; HIGH clear |
| SAFE / BRAKE-L / BRAKE-R | 9/10/11 | safety feedback; all four caster proofs grouped left/right |
| BALLAST-SECURED / CELL-CLOSED | 12/13 | restraint and interlocked test-cell proofs |
| BUTTON-UP / BUTTON-DOWN / RESET | 14/15/18 |3.3V dry contacts; spring return, reset fresh edge |
| IMU-SDA / IMU-SCL | 16/17 | GY521,3.3V pullups; WHOAMI68; +Z upward |
| OEM-HEALTHY | 21 | OEM-approved isolated healthy status |
| MOTION-HB | 38 | monitor only; removes on every software stop |
| PROP-ENGAGED | 39 | HIGH if EITHER pin engaged; inhibits both directions |

ESP32-S3-DevKitC-1-N8R8 is the India catalogue selection; the supplied PlatformIO
DevKitC target uses8MB flash and does not enable PSRAM. GPIO26..37, USB19/20 and
strap pins are excluded. Read the actual board revision silkscreen before wiring.
A generic ESP32, S3 Mini or WROOM2 board is not a drop-in substitution.

## Position conditioning subassembly (part of CONTROL kit)

Use Microchip MCP6002-I/P DIP8, listed by [Mouser India](https://www.mouser.in/en/ProductDetail/Microchip-Technology/MCP6002-I-P?qs=Ux5rHyN1IXStLRM979v6Rg%3D%3D).
The [manufacturer](https://www.microchip.com/en-us/product/MCP6002) specifies
rail-to-rail input/output and1.8..6V operation. This is a low-voltage bench circuit
for integrator review and measurement, not a safety-rated position channel.

```
3V3 --1kohm 1%-- POT-HI [Gefran5kohm] POT-LO --1kohm 1%-- GND
                        POT-WIPER -- U1 pin3 (+A)
                                     |--1Mohm 1%-- GND
U1 pin8=3V3; pin4=GND;100nF ceramic directly8-to4, plus1uF nearby
U1 pin1 OUT-A tied pin2 (-A); pin1 --100ohm-- ADC GPIO1
ADC GPIO1 --10kohm-- GND; ADC GPIO1 --100nF-- GND
Unused B: pin5=GND, pin6 tied pin7; no field24V connection
```

Use a soldered, inspected and enclosed board; verify package pinout/orientation
against current Microchip drawing. No socket/plug may invert the sensor supply.
The1Mohm wiper bias detects open wiper without the large nonlinear loading of the
previous direct10kohm connection. ADC10kohm remains after the buffer; calibrate its
linear divider effect.100ohm isolates ADC/filter capacitance from op-amp output.
At nominal5kohm sensor, unloaded endpoints are about0.471/2.829V, leaving fault
headroom. Input loading, op-amp offset, ADC attenuation/nonlinearity and component
variation still require the11-point <=2mm bench calibration; no measured accuracy
is claimed. Record actual3.3V and configure/check ADC attenuation on the real S3.

Absolute sensor mounting and stroke endpoints remain H06. Wire break/short to
rails must fault; a mechanically detached linkage can still read plausible values.
Keep independent travel limits. Supplied ADC endpoints400/3600 are placeholders;
measure and set actual values, preserving headroom. Do not commission by merely
installing the sensor. The board is included in the CONTROL RFQ; PCB layout,
connector protection and final harness inspection remain H09.

## Commissioning order

1. Keep supplied BENCH_COMMISSIONED=false. Run native and actual target compilation.
2. Complete labelled terminal-to-terminal as-built schematic, fuses, ratings,
   protective earth, isolation tests and OEM-approved interface, signed H02/H09.
3. Use lamps/instruments at every output; prove reset/startup and each independent
   stop including stuck MCU, stuck output and welded command contact.
4. Finish mechanical/guard holds, prove limits before endstops, calibrate sensors.
5. Locally enable only after signed unloaded release. Do not commit enabled defaults.
6. Limit individual jogs to <=8sec: software latches at10sec continuous command.
   Observe OEM duty cycle including repeated jogs; do not reset faults to evade it.

An initial industrial integrator RFQ is part of this package; a finished PCB,
complete harness terminal BOM and approved OEM pin assignment have NOT been created.
This is an explicit build blocker, not an instruction to improvise on a breadboard.
