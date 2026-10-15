# P0 bench wiring and integration

**No human use. No direct motor or 24 V wiring to the ESP32.** The selected OEM
actuator/control-box interface and independent safety circuit are not yet released.
This is a signal contract for an isolated bench fixture, not a complete wiring
approval. Do not replace the OEM controller's protection with the ESP32.

## Independent protections

- OEM matched actuator, controller, battery and charger with documented load
  retention, travel limits, overload/thermal protection, and emergency lowering.
- A hardwired E-stop and monitored safety circuit interrupt the OEM motion/run
  permission without relying on a GPIO instruction. Protective earth, fusing,
  isolation and supply ratings are determined from the selected system.
- Guard, support attachment and brake proofs belong in that hardware chain as
  engineered; the GPIO inputs are additional monitoring, not its only implementation.
- Direction-specific NC upper/lower travel switches inhibit the relevant OEM
  direction independently. Software limits supplement them.
- An independent edge-sensitive watchdog removes run permission on a missing or
  stuck heartbeat, including a CPU hung with UP and PERMIT still high. Its final
  timeout is derived from measured stopping travel; 100 ms is the bench design
  target, not a validated human safety value. A constant HIGH cannot satisfy it.
- Electrically/mechanically interlock opposite motion requests. No welded relay
  or single output fault may bypass the independent stop path. Choose the hardware
  safety architecture with the OEM/system engineer before applying loaded power.
- Mechanical wheel locks remain locked after power loss. Column safety nut/retention
  and a positive perch lock support static loads without active motor torque.
  Emergency lowering must not simply release a loaded carriage into free fall.

## ESP32-S3 DevKitC-1 signal map

Source of truth: [board_pins.h](../firmware/elderstep_controller/board_pins.h).
All contacts below are dry/isolated low-voltage signals. Never feed a 24 V status
line into a pin. Inputs use external 10 kΩ pulldowns as well as internal pulldowns.
Outputs require external pulldowns so reset/boot/disconnection removes requests.

| GPIO | Direction | Signal and healthy/active level |
| --- | --- | --- |
| 1 | ADC1 input | Absolute position wiper, ratiometric 3.3 V sensor; 10 kΩ pulldown detects open wiper as out of range |
| 4 | Output | Isolated OEM UP request, HIGH requests |
| 5 | Output | Isolated OEM DOWN request, HIGH requests |
| 6 | Output | Additional motion permission, HIGH requests |
| 7 | Input | Upper NC travel circuit, HIGH permits upward travel |
| 8 | Input | Lower NC travel circuit, HIGH permits downward travel |
| 9 | Input | Independent safety circuit feedback, HIGH healthy |
| 10 / 11 | Inputs | Left/right mechanical brake-group proofs, HIGH locked |
| 12 | Input | Engineered body-support attachment proof, HIGH secured |
| 13 | Input | Pinch guard proof, HIGH closed |
| 14 / 15 | Inputs | Caregiver UP/DOWN hold-to-run buttons, HIGH pressed |
| 16 / 17 | I2C | SDA/SCL, 3.3 V pullups, correctly oriented MPU6050 fixture IMU |
| 18 | Input | Deliberate reset button, HIGH pressed |
| 21 | Input | OEM controller health feedback, HIGH healthy |
| 38 | Output | Alternating heartbeat only during requested motion |
| 39 | Input | Positive mechanical perch lock proof, HIGH engaged, inhibits motion |

Brake groups must cover every wheel/swivel lock required by the stability design.
These single-channel GPIO contacts cannot detect every short or stuck switch.
The separate monitored hardware circuit must address such faults. An open perch
lock signal is not proof that the load is safely supported for unlocking/lowering.

No GPIO22/23/25 is used. GPIO34/35 are not ADCs on the S3. GPIO19/20 are left for
USB; flash/PSRAM GPIOs and strapping pins are avoided. Verify the exact board/module
variant against [Espressif's pin documentation](https://docs.espressif.com/projects/esp-idf/en/v5.0/esp32s3/api-reference/peripherals/gpio.html).

## Bench commissioning

1. Keep `BENCH_COMMISSIONED=false`. Compile and run native regression tests first.
2. Use LEDs/test instruments instead of motion outputs. Test boot, reset, every
   open contact, I2C loss, sensor disconnection and stuck output/watchdog behavior.
3. Identify exact OEM interfaces. Commission the independent stop and emergency
   lowering circuit with the supplier's permitted test fixture. Verify contact
   polarity and that no USB/backfeed can defeat power isolation.
4. Install an absolute transducer; measure ADC endpoints against external travel
   measurements. Set real travel, tilt orientation, progress threshold and timeouts.
   Position plausibility cannot detect a mechanically detached but electrically
   healthy sensor; test that fault and retain independent OEM limits.
5. Only after an engineer reviews the unloaded fixture and records its wiring,
   set `BENCH_COMMISSIONED=true` locally for unloaded bench motion. Do not commit
   a globally enabled default. The shipped values are placeholders.
6. Establish measured stopping travel and a safe physical test envelope. Progress
   to dummy loads only under [the validation plan](VALIDATION_PLAN.md).

Every boot and latched fault requires safe feedback stable for 500 ms, released
direction buttons, and a fresh reset edge. Hold-to-run release stops immediately
at the software output; physical stopping delay depends on the OEM system and
must be measured. No fault auto-resume or automatic homing is implemented.

The IMU must answer WHO_AM_I=0x68 and provide valid quasi-static acceleration
with +Z upward. A failed read removes permission; it does not reuse a default
level-floor measurement. The accelerometer supervisor is unsuitable for a future
walking mode without additional design and validation.

## Assembly release

There are no current manufacturing DXFs/STLs or issued tube lengths. Resolve
the mast/yoke moment load, seated support access, rest-lock unloading procedure,
guarding, full travel clearance, and stability before detailed CAD release.
The [historical geometry](../archive/pre-prototype/README.md) must not be ordered
as P0 parts. See [system drawing status](ASSEMBLY_BLUEPRINTS.md).
