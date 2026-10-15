# P0 validation and release record

Status on 15 October 2026: **software and CAD screening only; all physical gates open.**
Detailed [P0-B1 dummy procedures](p0b1/BENCH_TEST_PLAN.md) propose measurable
criteria and load stages; these are unperformed and require test-lead release.
No test in this repository authorizes use with a person. Successful source-level
tests do not establish sensor integrity, brake force, stop distance, clinical
suitability, or medical-device compliance.

## Release gates

| Gate | Required evidence | Current status |
| --- | --- | --- |
| G0 Requirements | Intended tasks, adult fit envelope, individual clinical constraints, actual home measurements, exclusions and measurable acceptance criteria | Provisional specification; not approved |
| G1 Design | Independent mechanical/system review; stability/load cases; exact OEM lift/support/lock compatibility; complete single-revision CAD/BOM; emergency recovery and guarding | Open; fabrication not released |
| G2 Unloaded bench | Electrical schematic inspection, interlock fault injection, boot/power loss/brownout, travel/position calibration, watchdog and welded/stuck output tests | Not performed |
| G3 Dummy loads | Instrumented static/dynamic/asymmetric loads across full travel and reach; retention, endurance, brake/slip, tipping and emergency lowering tests | Not performed |
| G4 Human study | Appropriate clinical/engineering approval, applicable regulatory/standards review, trained staff, consent and controlled study protocol | Not authorized |
| G5 Home use | Documented fit, route, user training, maintenance, support and applicable release evidence | Not authorized |

Assign numerical acceptance values before the corresponding physical test. Use
the applicable full standards and a qualified engineer rather than inventing
proof loads or safety factors here. ISO's public descriptions identify
[ISO 10535:2021](https://www.iso.org/standard/72711.html) for transfer hoists/body
supports and [ISO 11199-2:2021](https://committee.iso.org/standard/76652.html?browse=ics)
for rollators; a later gait configuration needs its own applicability review.
The full standards have not been purchased/reviewed in this repository and no
conformity is claimed. Jurisdictional classification and electrical/software
requirements remain to be determined for the final intended use.

## Software regression evidence

`python3 firmware/test_safety_interlocks.py` builds the actual C++ supervisor and
Arduino adapter using native hardware stubs, with address/undefined-behavior
sanitizers. Coverage includes both directions of every interlock loss, IMU loss
and stale/non-finite data, position errors, travel limits, neutral/restart rules,
fault recovery, a stuck position, wrong direction, loop/run timeouts and clock
rollover. The real firmware target must also compile via PlatformIO.

The tests cannot emulate contact welding, true motor transients, firmware timing
on loaded hardware, I2C electrical faults, or a load-bearing mechanical failure.
They do not count as clinical tests. Retain raw logs with commit/configuration
identifiers for each actual fixture test.

## Physical cases to test

### Lift and body support

- Full travel, worst-case yoke overhang and unilateral loading. Evaluate buckling,
  carriage binding, fasteners, welds, local bearing, latch engagement, fatigue,
  skin pressure and support slippage. Do not derive patient rating from axial thrust.
- Seated installation/removal without first making an unsupported person stand.
  Measure forward trunk clearance, knee/hip path, pinch zones and escape route.
- Stop the lift at multiple heights. Lose power, controller, one sensor and one
  contact in turn; prove secondary retention. Test the safe unlocking/unloading
  procedure for the perch lock, then controlled emergency lowering under dummy load.
- Hold the dummy at perch height with motor power removed. Measure creep and
  support pressure/duration, then perform controlled reach loads using cool props.

### Stability and floor interface

Use actual wheel contact coordinates and worst caster orientation, not outer
frame dimensions. Include the person/dummy's force application and center of
mass, offset stance, one-leg support, sideways reach, push/pull, and abrupt stops.
Evaluate overturning moments about every support-polygon edge. Evaluate sliding
separately: even a mechanically locked wheel can skid. Measure acceptable floors,
slopes and reach limits; P0 remains dry and level-floor only.

### Electrical and control faults

- Pull each contact wire, short it where plausible, stick each button, hold RESET
  during power-on, hold opposite commands, reset while a command is held.
- Remove IMU, freeze/rail/disconnect position signal, change sensor orientation,
  exceed tilt and direction limits, stall the actuator and block the guide.
- Cut/reapply supply and disconnect USB; verify no unexpected motion. Hang the CPU
  with active outputs and a constant heartbeat; prove the external watchdog stops
  OEM motion independently. Scope physical stopping travel, not only GPIO edges.
- Verify independent upper/lower limits, OEM overload/thermal protections, EMI
  behavior, duty cycle and charging isolation against the selected system's manual.

### Walking stage (G1–G4 must be repeated for changed configuration)

No occupied rolling in P0. A future gait trainer must preserve body support while
changing wheel-brake state, expose the complete stride/foot path, and use a
validated walking support rather than a thigh-blocking perch seat. Test force
transfer, tipping, runaway, stopping, fatigue and independent recovery during
stepping. A clinician determines whether non-weight-bearing gait, partial loading,
or another mobility aid is appropriate. No preset week-by-week recovery schedule.

## Test record template

Record: requirement ID; drawing and firmware revision; exact part serials;
calibration; dummy mass/geometry; floor and fixture; method; predeclared limit;
measured result; anomaly; reviewer; date; disposition. An unchecked row means
unverified, not passed. Publish failures and repairs before repeating a gate.
