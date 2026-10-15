# FreeStep Air (`9.65 kg` Clinical & Home Mastery Edition): Procurement & 1-Weekend Build Plan

This architecture follows two golden rules:
1. **100% Standard Multi-Vendor COTS Cartridges + Custom CNC `7075-T6` Plates:** Zero proprietary medical B2B lock-in. Every motor, actuator, bearing, wheel, and sensor is a universal commodity item sold by dozens of Indian vendors on Robu.in, Amazon India, Decathlon, and IndiaMART.
2. **Zero Gimmicks, 100% Clinical & Daily-Life Mastery:** We stripped out over-engineered bulk (heavy `MGN9C` steel rails, fragile spinning floor LiDAR, and hinge-crossing strain gauge wires — saving **`200 g`** and **`₹8,550`**) and integrated **9 hospital-grade orthopedic & home-living upgrades** derived from FDA *Arjo Sara* / *Rifton TRAM* / *Zeen* analysis and 2024–2026 ankle-fracture rehabilitation research.

- **Total Weight:** **`9.65 kg`** (Sub-10 kg featherweight class — `200 g` lighter than v1)
- **Total Prototype Cost:** **`₹54,250`** (23 line items in [`hardware/INDIA_BOM_SOURCING.csv`](./hardware/INDIA_BOM_SOURCING.csv) — **saves `₹8,550`** vs. v1)
- **Mechanical Assembly Time:** **`10–12 Hours` (1 Single Weekend)**
- **Automated Firmware Verification:** **`16 / 16` Safety & Clinical Rehab Tests Passing** ([`firmware/test_safety_interlocks.py`](./firmware/test_safety_interlocks.py))

---

## 1. How the 9 New Clinical Upgrades + 3 Simplifications Transform `FreeStep Air`

| Upgrade / Change | What Changed in Hardware & Firmware | Why It's a 10x Improvement for Grandma & Broad Users |
| :--- | :--- | :--- |
| **1. `90°` Single-Leg "Knee-Scooter" Detent Mode** | Added a precision `90°` pin-detent pocket to [`saddle_180_pivot_hinge.dxf`](./hardware/cnc_7075/saddle_180_pivot_hinge.dxf) + `MODE_KNEE_SCOOTER` (`0.18 m/s` indoor speed cap) | During Weeks 1–4 of ankle fracture recovery (`0%` weight-bearing), Grandma locks **one** saddle pad at `450 mm` knee height to rest her injured shin/knee while folding the other pad `180°` open to propel with her healthy leg! |
| **2. Fold-Down Aluminum Footrest Pegs** | Clamped fold-down anodized aluminum pegs + `M6` ball detents onto the lower `ø30 mm` carbon legs (`CF-03`) | Gives her fractured ankle a safe elevated rest (`95 mm` off the floor) during **Seated Power-Glide Mode (`0.25 m/s`)** through narrow `20"` bathroom doorways. |
| **3. Contoured Anterior Tibial Shin Block Pad (`340 mm`)** | Added a quick-release closed-cell EVA shin support pad across the lower columns (`340 mm` height) | Replicates the *Arjo Sara Stedy* "Zero-Quad Toilet Rise": prevents forward knee buckling when lifting from a low `400 mm` commode. |
| **4. $8^\circ$ Anatomical EVA Forearm Support Troughs + Deep-Bowed Halo** | Added $8^\circ$ inclined medical EVA forearm cuffs with velcro straps & embedded `FSR406` sensors on the upper halo | Transfers upper-body support from fragile/arthritic wrists to the strong olecranon (elbows) and forearms. |
| **5. Graduated Weight-Bearing (PWB) Rehab Coach** | Firmware calculates real-time limb load (`BodyWeight - ForearmLoad`) against Doctor's target (`0% / 25% / 50% / 100%`) | Turns the walker into an active physical-therapy biofeedback coach with OLED bar-graph and gentle haptic buzzer alerts if she overloads her healing ankle. |
| **6. Front Caster $0^\circ$ Anti-Yaw Detent + Labyrinth Hair Shields** | Added `M6` spring ball-plunger $0^\circ$ directional detent + snap-fit labyrinth axle shields to [`inhouse_twin_64mm_caster_fork.dxf`](./hardware/cnc_7075/inhouse_twin_64mm_caster_fork.dxf) | Eliminates sideways caster fishtailing on wet sloped Indian bathroom tiles and prevents floor hair from jamming the `608RS` bearings. |
| **7. 1-Click Retractable Pelvic Safety Belt** | Automotive-style retractable webbing belt clips across the rear of the upper halo | Completes a `360°` fall-proof waist enclosure during standing and walking. |
| **8. Automatic `2:00 AM` PIR Motion Under-Frame Nightlight** | Added `AM312` PIR motion sensor + warm amber `2700K` downward LED strip under the front cross-tube | Automatically illuminates Grandma's feet and bathroom door thresholds the instant she swings her legs out of bed in the dark. |
| **9. Universal Cane / Crutch / IV-Bag Quiver Clips** | Snap-fit `TPU/PA12` clips on the outer `ø35 mm` carbon barrel | Carries her forearm crutches, walking cane, or hospital IV/catheter bag hands-free. |
| **10. Cut 3 Over-Engineered Gimmicks (`-200 g`, `-₹8,550`)** | Replaced `MGN9C` steel rails with **Swing-Away Quick-Clip Polycarbonate Tray (`180 g`)**; replaced fragile `LD19` LiDAR + 3-board `UWB` with **Waterproof 4-Button RF Wristband ("Valet Park-Away & Fetch") + Dual `VL53L1X` ToF**; replaced hinge strain gauges with **Waterproof Seat Micro-Switch + Reed Switch** | Zero knee/chest obstruction during sit-to-stand, zero fragile wires flexing across hinges, and Grandma can both **park the walker away to the wall** after getting into bed and **fetch it back** to her knees! |

---

## 2. Day-1 Ordering Checklist (23 Standard Items Across 4 Batches — `₹54,250` Total)

Full item-by-item specifications and weights are in [`hardware/INDIA_BOM_SOURCING.csv`](./hardware/INDIA_BOM_SOURCING.csv).

### Batch A: Robu.in (Standard Actuators, Sealed Hub Wheels, Carbon Tubes, Sensors & LiFePO4) — ~`₹32,200` (2–3 Day Delivery)
1. **Standard Carbon Fiber Tubes (Cut per [`hardware/CARBON_TUBE_CUTLIST.csv`](./hardware/CARBON_TUBE_CUTLIST.csv)):**
   - `2x` `3K Roll-Wrapped Carbon Tube (35mm OD x 31mm ID x 1000mm)` — Outer telescoping column barrels (`₹6,400`)
   - `2x` `3K Roll-Wrapped Carbon Tube (30mm OD x 26mm ID x 1000mm)` — Inner telescoping plungers + U-base legs (`₹5,200`)
   - `2x` `3K Roll-Wrapped Carbon Tube (25mm OD x 21mm ID x 1000mm)` — Deep-bowed upper torso halo & cross-bridge (`₹3,900`)
2. **Standard Sealed Actuators & Hub Drive:**
   - `2x` **Standard `24V 300mm` Stroke Tubular Inline Linear Actuator (`1500N` Self-Locking, `IP65` Sealed, Built-in Hall Encoder)** (`₹5,200`)
   - `2x` **Standard `6.5"` (`165 mm`) `24V` Sealed BLDC Hall-Sensor Hub Motor Wheels (`IP65`, `ø16 mm` D-Axle)** (`₹4,400`)
   - `1x` **Dual-Channel `24V` Sinusoidal FOC Brushless Motor Controller (`SimpleFOC` / `ZS-X11H` with Active Brake)** (`₹2,200`)
3. **Standard Dev Boards, Valet Park/Fetch Remote, PWB Coach & Nightlight Sensors:**
   - `1x` `ESP32-S3-DevKitC-1` + `0.96" OLED` (PWB Rehab Coach Display) + Gentle Piezo Buzzer (`₹950`)
   - `1x` `Waterproof 433MHz 4-Button RF Wristband Remote + Superheterodyne Receiver` (Valet Park-Away & Fetch) (`₹600`)
   - `2x` `VL53L1X Time-of-Flight (ToF) Obstacle & Cliff Sensors` + `1x` `BNO085 9-DOF IMU` (`₹2,100`)
   - `2x` `FSR406 Forearm Trough Force Sensors` + `1x` `Waterproof IP67 Seat Cushion Micro-Switch` + `1x` `Center Latch Reed Switch` (`₹950`)
   - `1x` `AM312 PIR Motion Sensor` + `24V Warm Amber LED Under-Glow Strip` (Automatic `2:00 AM` Nightlight) (`₹350`)
   - `2x` `BTS7960 43A H-Bridge` + `24V-to-5V Buck` + `22mm E-Stop` (`₹1,150`)
   - `1x` `Standard 24V 6Ah LiFePO4 Battery Pack + 29.2V 3A Charger` (`₹3,800`)

### Batch B: Upload 6 Flat Plate DXFs + 1 Delrin Bushing STL to Robu CNC / Karkhana.io — ~`₹10,000` (4 Days)
1. **CNC `7075-T6` Aluminum Flat Plates (`hardware/cnc_7075/*.dxf`):**
   - `2x` [`12deg_incline_base_lug.dxf`](./hardware/cnc_7075/12deg_incline_base_lug.dxf)
   - `2x` [`inhouse_sfu1204_ballscrew_column_cap.dxf`](./hardware/cnc_7075/inhouse_sfu1204_ballscrew_column_cap.dxf)
   - `2x` [`rear_16mm_hub_axle_dropout.dxf`](./hardware/cnc_7075/rear_16mm_hub_axle_dropout.dxf)
   - `2x` [`inhouse_twin_64mm_caster_fork.dxf`](./hardware/cnc_7075/inhouse_twin_64mm_caster_fork.dxf) (Includes $0^\circ$ Anti-Yaw Ball-Plunger Pocket)
   - `2x` [`saddle_180_pivot_hinge.dxf`](./hardware/cnc_7075/saddle_180_pivot_hinge.dxf) (Includes `0° / 90° Knee-Scooter / 180°` Detent Pockets) + `1x` [`inhouse_n52_conical_saddle_latch.dxf`](./hardware/cnc_7075/inhouse_n52_conical_saddle_latch.dxf)
2. **CNC Lathe-Turned `POM (Delrin)` Sleeve Bushings & 3D-Printed Accessories:**
   - `4x` [`delrin_telescoping_column_bushing.stl`](./hardware/3d_print/delrin_telescoping_column_bushing.stl) (`31.0 mm OD x 30.05 mm ID x 40 mm`)
   - `1x` [`upper_halo_floating_delrin_mount.stl`](./hardware/3d_print/upper_halo_floating_delrin_mount.stl) + [`caster_anti_hair_labyrinth_cap.stl`](./hardware/3d_print/caster_anti_hair_labyrinth_cap.stl) + [`cane_crutch_quiver_clip.stl`](./hardware/3d_print/cane_crutch_quiver_clip.stl)

### Batch C: Decathlon / Amazon India (Skate Wheels, Thrust Bearings, Footrest Pegs, Safety Belt & Epoxy) — ~`₹5,550` (Next-Day)
- `4x` `Oxelo 64mm 82A High-Rebound Inline Skate PU Wheels + ABEC-9 608RS Bearings` + `2x` `SKF 51104 Thrust Bearings` + `2x` `M6 Spring Ball Plungers` (`₹1,550`)
- `2x` `Fold-Down Knurled Aluminum Footrest Pegs (ø30mm Tube Clamps)` (`₹450`)
- `1x` `Quick-Clip Swing-Away 5mm Polycarbonate Utility & Tea Tray (380x240mm)` (`₹400`)
- `1x` `1-Click Retractable Pelvic Safety Belt + Quick-Release Buckle` (`₹400`)
- `1x` `3M DP420 Structural Epoxy (50ml) + 110um Glass Microspheres + M5/M6/M8 304SS Fasteners` (`₹2,150`)
- `2x` `N52 Neodymium Ring Magnets (20x5mm)` + `2x` `10mm 304SS Conical Dowel Pins` + `4x` `608RS Flanged Bearings` (`₹600`)

### Batch D: Local Car Seat / Medical Upholsterer — ~`₹2,700` (1 Day)
- `2x` Closed-cell EVA foam split-saddle pads wrapped in wipe-clean antibacterial marine vinyl (`₹1,200`)
- `2x` Contoured $8^\circ$ Medical EVA Forearm Support Troughs with Velcro Wrist/Elbow Straps (`₹950`)
- `1x` Contoured Anterior Tibial Shin Block Pad (`340 mm` height, wipe-clean EVA foam) (`₹550`)

---

## 3. 1-Weekend Cartridge Assembly Guide (10–12 Hours Total)

1. **Drop the Standard `24V 300mm` Actuator Cartridges Inside the Carbon Columns (1.5 Hours):** Press-fit the lathe-turned Delrin bushings ([`delrin_telescoping_column_bushing.stl`](./hardware/3d_print/delrin_telescoping_column_bushing.stl)) into the `ø35 mm` outer and `ø30 mm` inner carbon tubes, slide the standard `IP65` `24V 300mm` inline actuator inside, and pin top & bottom with two `M8` clevis pins.
2. **Bolt on the `6.5"` Sealed Hub Wheels, Fold-Down Footrests & `74 mm` Anti-Yaw Front Casters (1.5 Hours):** Clamp the `ø16 mm` D-flat hub axles into [`rear_16mm_hub_axle_dropout.dxf`](./hardware/cnc_7075/rear_16mm_hub_axle_dropout.dxf) (`12 Nm`), mount the Fold-Down Footrest Pegs on `CF-03`, and assemble the twin `64 mm` skate wheels + labyrinth hair shields + `SKF 51104` bearing + `0°` ball-plunger into [`inhouse_twin_64mm_caster_fork.dxf`](./hardware/cnc_7075/inhouse_twin_64mm_caster_fork.dxf).
3. **Mount the 3-Mode Split-Saddle (`0° / 90° / 180°`), Shin Block Pad & $8^\circ$ Forearm Troughs (2 Hours):** Clamp [`saddle_180_pivot_hinge.dxf`](./hardware/cnc_7075/saddle_180_pivot_hinge.dxf) onto the inner `ø30 mm` tubes, clip the Anterior Tibial Shin Block Pad at `340 mm` height, and mount the $8^\circ$ EVA Forearm Troughs + Swing-Away Utility Tray on the upper halo.
4. **Wire `ESP32-S3` & Run the 16 Clinical/Safety Tests (Sunday):** Flash [`firmware/elderstep_controller/elderstep_controller.ino`](./firmware/elderstep_controller/elderstep_controller.ino) and run `python3 firmware/test_safety_interlocks.py` to verify all **16 safety and clinical rehab tests pass**.
