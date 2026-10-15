# P0 redesign decisions and issue disposition

The current direction is **caregiver-assisted rise, controlled sitting and
stationary kitchen perch**. The first prototype is bench-only, not a clinically
validated product. [Current product research](research/CURRENT_PRODUCTS_AND_DESIGN.md)
and [the authoritative specification](hardware/PROTOTYPE_SPEC.md) define why.

| Earlier issue | P0 resolution | What remains |
| --- | --- | --- |
| Disagreeing parallelogram/carbon telescoping designs | One guided single-lift architecture; old geometry/viewers quarantined | Reviewed CAD and full load-path design |
| Dual lift pulse counters increased when lowering; no reliable absolute height | Remove dual lift and pulse homing; use an absolute transducer | Calibrate real sensor, independent OEM limits, fault tests |
| IMU loss silently allowed motion | Missing/stale/invalid IMU latches a stop; no default healthy readings | Physical wiring/orientation and common-cause fault review |
| Spin bypassed cliff checks; auto-lowering could keep running after a stop | Remove drivetrain, spin, summon and cliff modes; every supervisor stop clears all lift requests | Independent stop circuit and watchdog must work on real hardware |
| Invalid ESP32-S3 GPIO/ADC assignments | Use exposed S3 GPIOs and ADC1 GPIO1; compile actual board target | Verify exact purchased board and isolated interfaces |
| Passing tests duplicated a more capable Python model | Compile/test the same C++ core and actual Arduino adapter | Native stubs cannot prove hardware or clinical safety |
| Software/hub braking called fail-safe | Passive mechanical wheel locks plus OEM lift retention; no electronic wheel brake claim | Measure skid/tip/hold under worst loads/floors |
| 495 mm treated as universally stable/home-compatible | Size base from fit and loaded stability; home-route gate | Real measurements and testing; narrow door fit not promised |
| “PWB coach” inferred ankle force from forearms | Remove clinical loading computation and feedback | Limb-specific measurement research, if later justified |
| Knee-scooter and powered seated transport added multiple failure cases | Removed from P0; walking separately specified as future validation | Dedicated support continuity/gait work |
| 9.65 kg/₹54,250/12-hour/hospital-grade/fall-proof claims | Withdrawn; quote-based BOM with explicit unknowns | Actual supplier quotes, measured mass, full validation |
| STL plate bores absent; incomplete latch/clamp geometry | P0-B1 bored STEP/DXF review exports; legacy generators saved as reference text | Complete reviewed geometry and export comparisons |

## Why one lift and an OEM controller

Removing synchronization is simpler than patching incremental counters and hoping
two actuators stay level. A guided carriage carries moments independently of the
actuator. The OEM system must supply its own retention, limits, protection and
emergency lowering. The ESP32 remains a non-safety-rated bench supervisor, with
hardware protection independent of its outputs.

## First walking stage

Research supports a later manual gait configuration with continuous pelvic and
forearm support, stride clearance and controlled mechanical braking. The active
P0 controller requires wheel locks engaged; it is not suitable for occupied
rolling. Do not add a “walk” button without reviewing the changed load cases.

## Remaining release blockers

P0-B1 selects an actuator/guide and bench frame dimensions. No safe working load,
human support pairing,
rest-lock unloading mechanism, safety circuit or production drawing is approved.
These cannot be settled by rewriting documentation or compiling firmware.
Follow [the validation gates](hardware/VALIDATION_PLAN.md) before fabrication,
loaded trials and any human study.

P0-B1 now adds editable bench CAD, India source evidence, dimensional drawings,
assembly/weld mapping, screw-prop recovery, geometry screening and dummy procedures.
See [the package](hardware/p0b1/README.md) for remaining supplier/engineering holds.
