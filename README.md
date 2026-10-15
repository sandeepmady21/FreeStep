# FreeStep P0 — assisted rise and kitchen perch

**Status: bench engineering prototype; no human-use release, load rating, or fabrication release.**

The first prototype focuses on caregiver-assisted sit-to-stand, controlled sitting,
and a stationary supported kitchen perch. One guided lift replaces the two DIY
actuators. Mechanical wheel locks replace powered hub motors. The controller is
disabled by default and requests motion from a separately protected OEM lift system.

The intended future user can contribute to standing through at least one leg.
Adjustability is a design requirement, not a claim that one size fits everyone.
The initial design study covers adults approximately 150–185 cm and 50–100 kg;
these are provisional fit targets, **not a tested population or safe working load**.
Clinical weight-bearing restrictions remain individual.

## Start here

| Document | Purpose |
| --- | --- |
| [Product research](research/CURRENT_PRODUCTS_AND_DESIGN.md) | Current commercial products, availability caveats, sit-to-stand mechanics, and a staged walking solution; checked 15 October 2026 |
| [Prototype specification](hardware/PROTOTYPE_SPEC.md) | One authoritative architecture, adjustments, use sequence, and exclusions |
| [Hardware and wiring](hardware/WIRING_AND_ASSEMBLY_GUIDE.md) | Independent safety circuit and actual ESP32-S3 pin map |
| [Validation plan](hardware/VALIDATION_PLAN.md) | Evidence required before fabrication, loaded testing, and any human study |
| [Procurement](PROCUREMENT_AND_BUILD_PLAN.md) | Quote-based BOM, supplier questions, and staged construction |
| [Change rationale](IMPROVEMENT_PLAN.md) | Findings addressed and remaining limitations |

## What is implemented

- A single-lift C++ supervisor shared by the Arduino firmware and native tests.
- Hold-to-run up/down; deliberate reset after boot/fault; neutral required before
  reversing or restarting after a limit or perch-lock stop.
- Brake, body-support attachment, guard, OEM health, and hardware safety feedback.
- Absolute position instead of increment-only Hall counters; direction limits,
  stale/missing/invalid IMU rejection, tilt stop, progress and run timeouts.
- Every stop removes **all** lift requests and the external watchdog heartbeat.
- No powered wheels, autonomous fetch, knee-scooter mode, width morphing, or
  inferred ankle-loading measurements.

The ESP32 is **not a safety-rated controller**. Firmware tests cannot validate
the physical device. A monitored hardware safety circuit, OEM protections,
mechanical load retention, and independent emergency lowering remain required.

## Run software verification

```sh
python3 firmware/test_safety_interlocks.py
python3 tools/validate_repository.py
```

The first command compiles the actual C++ core and Arduino adapter with GPIO/I2C
stubs, using a C++17 compiler plus address/undefined-behavior sanitizers. It does
not run a separate Python model. The second checks active documentation links,
pin assignments, BOM completeness, and disabled commissioning defaults.

Compile the actual ESP32-S3 firmware with [PlatformIO](https://docs.platformio.org/):

```sh
pio run -e esp32s3_bench
```

`BENCH_COMMISSIONED=false` is intentional. See
[bench commissioning](hardware/WIRING_AND_ASSEMBLY_GUIDE.md#bench-commissioning).
Changing it never authorizes testing with a person.

## Walking is a separate validation stage

P0 permits only unoccupied manual repositioning, then locks the frame for rise
and perch. It does not transport an occupied user or authorize gait practice.
The [research report](research/CURRENT_PRODUCTS_AND_DESIGN.md#how-to-add-walking)
explains how continuous pelvic support, stride clearance, mechanical braking,
and clinical assessment would enable a later walking prototype. Until then,
walking uses a separately assessed commercial aid and an assisted transfer.

## Original FreeStep and historical concepts

The original [STEP model](Models/FreeStep.step) and
[images](Images/FreeStep_open.jpg) are retained for attribution and study. They
are **not P0 manufacturing files**. The original project is
[htx-studio/FreeStep](https://github.com/htx-studio/FreeStep), under the included
[MIT license](LICENSE). See also the original
[video reference](https://www.bilibili.com/video/BV17TEC6AE3Z/).

Previous BOMs, generated geometry, plans, viewer, firmware, and model tests are
preserved in [archive/pre-prototype](archive/pre-prototype/README.md). Their
9.65 kg, ₹54,250, 12-hour build, clinical suitability, and fall-proof claims are
withdrawn. No complete P0 CAD assembly or manufacturing cutlist has been released.
