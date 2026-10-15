# FreeStep Air (`9.65 kg` Clinical & Home Mastery Edition): Master Assembly Blueprints (Sheets 1–6)

All 6 engineering assembly blueprints below are scaled for the **100% Standard Multi-Vendor COTS Cartridge + 9 Clinical Upgrades Architecture** (`₹54,250` total cost, `9.65 kg` total mass, `10–12 hour` single-weekend build).

You can also open the interactive 3D WebGL CAD assembly & part inspector in your browser at [`docs/assembly_blueprints.html`](../docs/assembly_blueprints.html).

---

## Sheet 1 of 6: Master Chassis Orthographic & Clinical Biomechanics
![Blueprint 01: Master Frame Orthographic](./blueprints/blueprint_01_master_frame_orthographic.svg)

* **Outer Width:** Fixed **`495.0 mm (19.5")`** — clears every `510 mm (20.0")` Indian bathroom doorway with zero width-morphing motors.
* **Inside Hip/Toilet Clearance:** **`430.0 mm (17.0")`** — backs directly over standard Indian & Western commodes.
* **Zero-Quad Toilet Rise:** Combines **$12.0^\circ$ forward-inclined columns** (`+293 mm` vertical lift + `+62 mm` forward CG shift) with a **Contoured Anterior Tibial Shin Block Pad (`340 mm` height)** so Grandma's knees never buckle forward when rising from a low `400 mm` commode.
* **$8^\circ$ Anatomical Forearm Troughs + Fold-Down Footrest Pegs:** Offloads fragile wrists onto her elbows/forearms and supports her fractured ankle safely off the floor during Seated Power-Glide.

---

## Sheet 2 of 6: Telescoping Carbon Column & Standard `24V 300mm` Actuator Cartridge
![Blueprint 02: Telescoping Carbon Actuator Column](./blueprints/blueprint_02_telescoping_carbon_actuator_column.svg)

* **Structural Secret (Bending Decoupling):** Standard tubular inline linear actuators cannot take side bending loads on their own. By sliding the **Standard `24V 300mm` `IP65` Inline Linear Actuator (`ACT-01`)** inside our **`ø35 mm` outer (`CF-01`) and `ø30 mm` inner (`CF-02`) 3K roll-wrapped carbon tubes** gliding on **CNC lathe-turned `POM (Delrin)` sleeve bushings ([`delrin_telescoping_column_bushing.stl`](./3d_print/delrin_telescoping_column_bushing.stl))**, the carbon tubes absorb **100% of lateral and bending forces** while the sealed actuator inside pushes purely axially via two **`M8` quick-release clevis pins**.
* **Universal Cane / Crutch / IV-Bag Quiver Clips:** Snap directly onto the `ø35 mm` outer carbon barrel.

---

## Sheet 3 of 6: Rear `6.5"` (`165 mm`) Sealed `IP65` BLDC Hub Wheel, Dropout & Fold-Down Footrests
![Blueprint 03: Rear 6.5in Hub Wheel Dropout](./blueprints/blueprint_03_rear_65in_hub_wheel_dropout.svg)

* **CNC Part:** [`rear_16mm_hub_axle_dropout.dxf`](./cnc_7075/rear_16mm_hub_axle_dropout.dxf) (`12 mm` thick `7075-T6` aluminum).
* **Standard Wheel:** Commodity `6.5"` (`165 mm`) `24V` Hall-sensor brushless hub wheel (`IP65` waterproof, universal `ø16 mm` D-flat shaft).
* **3 Active Drive Modes:** (1) Effortless Walking & Slope Assist, (2) **Seated Power-Glide (`0.25 m/s`)** with feet resting on the **Fold-Down Aluminum Footrest Pegs**, and (3) **`40 Nm` Electronic Dead-Man's Hold Brake**.

---

## Sheet 4 of 6: Ultra-Low `74 mm` Front Caster + $0^\circ$ Anti-Yaw Detent & Labyrinth Hair Shields
![Blueprint 04: Front 74mm Twin Skate Caster](./blueprints/blueprint_04_front_74mm_twin_skate_caster.svg)

* **CNC Part:** [`inhouse_twin_64mm_caster_fork.dxf`](./cnc_7075/inhouse_twin_64mm_caster_fork.dxf) (`10 mm` thick `7075-T6` aluminum).
* **Solves the #1 *Arjo Sara* & Home Caster Failures:**
  1. **$0^\circ$ Ball-Plunger Directional Detent:** Keeps the front casters tracking straight along hallways and sloped wet bathroom tiles without sideways fishtailing, while breaking out smoothly above `18 N` lateral force for `360°` spin-in-place turns.
  2. **Labyrinth Anti-Hair Axle Shields:** Prevents floor hair and dust from wrapping around the `M8` axle and seizing the `ABEC-9 608RS` bearings.

---

## Sheet 5 of 6: `180°` Split-Saddle, `90°` Knee-Scooter Detent & `N52` Conical Shear Latch
![Blueprint 05: Split Saddle 180 Hinge and Latch](./blueprints/blueprint_05_split_saddle_180_hinge_and_latch.svg)

* **CNC Parts:** [`saddle_180_pivot_hinge.dxf`](./cnc_7075/saddle_180_pivot_hinge.dxf) + [`inhouse_n52_conical_saddle_latch.dxf`](./cnc_7075/inhouse_n52_conical_saddle_latch.dxf).
* **3 Instant Positions:**
  1. **`180°` Open Walk-In / Commode Mode:** Both pads fold flush against the side carbon columns (`430 mm` unobstructed clearance).
  2. **`90°` Single-Leg Ankle-Fracture Knee-Scooter Mode:** One pad locks at `90°` (`450 mm` knee height) to support Grandma's fractured ankle `100%` off the floor while the other pad folds `180°` out of the way so her healthy leg can propel!
  3. **`0°` Latched Perch / Transfer Mode:** Both pads snap together via `N52` magnets + **twin `10 mm` `304` stainless `45°` conical shear pins (`12 kN` / `1,200 kgf` shear capacity)** + **Retractable Pelvic Safety Belt**.

---

## Sheet 6 of 6: $8^\circ$ Forearm Troughs, Swing-Away Tray, PWB Rehab Coach & `ESP32-S3` Wiring
![Blueprint 06: Kitchen Tray and Electronics Wiring](./blueprints/blueprint_06_kitchen_tray_and_electronics_wiring.svg)

* **2-Second Quick-Clip Swing-Away Utility Tray (`180 g`):** Replaces heavy `MGN9C` steel rails (`-500 g`, `-₹1,400`), swinging `90°` out of the way so it never blocks torso lean during sit-to-stand or foot visibility during walking.
* **Graduated Weight-Bearing (PWB) Rehab Coach:** Uses the forearm trough `FSR406` sensors + OLED/buzzer to coach Grandma through her orthopedic surgeon's `0% -> 25% -> 50% -> 100%` ankle loading schedule.
* **Waterproof 4-Button RF Wristband ("Valet Park-Away & Fetch") + `2:00 AM` PIR Nightlight:** Lets Grandma send the walker away to the wall after getting into bed and fetch it back to her knees, while Dual `VL53L1X` ToF sensors guard against obstacles and stairs.
