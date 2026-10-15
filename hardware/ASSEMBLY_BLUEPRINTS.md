# FreeStep Air (`9.85 kg` Standard-COTS Edition): Master Assembly Blueprints (Sheets 1–6)

All 6 engineering assembly blueprints below are scaled for the **100% Standard Multi-Vendor COTS Cartridge Architecture** (`₹62,800` total cost, `9.85 kg` total mass, `10–12 hour` single-weekend build).

You can also open the interactive exploded CAD blueprint viewer in your browser at [`docs/assembly_blueprints.html`](../docs/assembly_blueprints.html).

---

## Sheet 1 of 6: Master Chassis Orthographic & Kinematic Envelope
![Blueprint 01: Master Frame Orthographic](./blueprints/blueprint_01_master_frame_orthographic.svg)

* **Outer Width:** Fixed **`495.0 mm (19.5")`** — clears every `510 mm (20.0")` Indian bathroom doorway with zero width-morphing motors.
* **Inside Hip/Toilet Clearance:** **`430.0 mm (17.0")`** — backs directly over standard Indian & Western commodes.
* **Front Under-Bed Nose Height:** **`74.0 mm (2.9")`** — slides under low beds and sofas.
* **$12.0^\circ$ Forward-Inclined Columns:** `300 mm` stroke produces **`+293 mm` vertical lift** (`420 mm` $ightarrow$ `713 mm` saddle height) and **`+62 mm` natural forward weight shift** ("Nose-Over-Toes" biomechanics).

---

## Sheet 2 of 6: Telescoping Carbon Column & Standard `24V 300mm` Actuator Cartridge
![Blueprint 02: Telescoping Carbon Actuator Column](./blueprints/blueprint_02_telescoping_carbon_actuator_column.svg)

* **Structural Secret (Bending Decoupling):** Standard tubular inline linear actuators cannot take side bending loads on their own. By sliding the **Standard `24V 300mm` `IP65` Inline Linear Actuator (`ACT-01`)** inside our **`ø35 mm` outer (`CF-01`) and `ø30 mm` inner (`CF-02`) 3K roll-wrapped carbon tubes** gliding on **CNC lathe-turned `POM (Delrin)` sleeve bushings ([`delrin_telescoping_column_bushing.stl`](./3d_print/delrin_telescoping_column_bushing.stl))**, the carbon tubes absorb **100% of Grandma's lateral and bending forces** while the sealed actuator inside pushes purely axially via two **`M8` quick-release clevis pins**.
* **3-Minute Serviceability:** Pull the top and bottom `M8` clevis pins to slide the standard actuator cartridge out in 3 minutes.

---

## Sheet 3 of 6: Rear `6.5"` (`165 mm`) Sealed `IP65` BLDC Hub Wheel & `ø16mm` Dropout
![Blueprint 03: Rear 6.5in Hub Wheel Dropout](./blueprints/blueprint_03_rear_65in_hub_wheel_dropout.svg)

* **CNC Part:** [`rear_16mm_hub_axle_dropout.dxf`](./cnc_7075/rear_16mm_hub_axle_dropout.dxf) (`12 mm` thick `7075-T6` aluminum).
* **Standard Wheel:** Commodity `6.5"` (`165 mm`) `24V` Hall-sensor brushless hub wheel (`IP65` waterproof, universal `ø16 mm` D-flat shaft).
* **Why It's Safe for Indian Homes:** 100% enclosed shell—zero exposed belts or spinning motor bells to snag Grandma's saree or nightgown, and completely sealed against wet bathroom floors.
* **Torque Spec:** Torque the four `M6x35` Grade 10.9 axle clamp bolts with Blue Loctite 243 to **`12.0 Nm`**.

---

## Sheet 4 of 6: Ultra-Low `74 mm` Front Twin-Skate Caster Assembly
![Blueprint 04: Front 74mm Twin Skate Caster](./blueprints/blueprint_04_front_74mm_twin_skate_caster.svg)

* **CNC Part:** [`inhouse_twin_64mm_caster_fork.dxf`](./cnc_7075/inhouse_twin_64mm_caster_fork.dxf) (`10 mm` thick `7075-T6` aluminum).
* **Standard Parts:** `SKF 51104` axial thrust ball bearing (`20x35x10 mm`) + twin Decathlon `Oxelo 64 mm 82A` high-rebound polyurethane inline-skate wheels with `ABEC-9 608RS` sealed bearings.
* **Why Twin `64 mm` Wheels:** Cuts swivel scrubbing friction in half on wet/dry bathroom tiles, rolls silently over tile grout lines, and easily climbs `15–40 mm` marble thresholds while keeping the front nose at **`74.0 mm (2.9")`**.

---

## Sheet 5 of 6: `180°` Split-Saddle Pivot Hinge & `N52` Conical Stainless Shear Latch
![Blueprint 05: Split Saddle 180 Hinge and Latch](./blueprints/blueprint_05_split_saddle_180_hinge_and_latch.svg)

* **CNC Parts:** [`saddle_180_pivot_hinge.dxf`](./cnc_7075/saddle_180_pivot_hinge.dxf) + [`inhouse_n52_conical_saddle_latch.dxf`](./cnc_7075/inhouse_n52_conical_saddle_latch.dxf).
* **How It Works:**
  * **Open Walking / Toilet Mode:** Both cushioned saddle halves swing **`180°` outward** flush against the side carbon columns, giving Grandma a completely open `430 mm` walk-in bay.
  * **Seated Transfer / Kitchen Perch Mode:** Swing both halves inward—the `N52` ring magnets (`20x5 mm`) self-center and snap the **twin `10 mm` `304` stainless steel `45°` conical shear pins** into their mating tapered sockets (**`12 kN` / `1,200 kgf` mechanical shear strength**).

---

## Sheet 6 of 6: `MGN9C` Slide-Bridge Kitchen Tray, Anti-Bind Float & `ESP32-S3` Master Wiring
![Blueprint 06: Kitchen Tray and Electronics Wiring](./blueprints/blueprint_06_kitchen_tray_and_electronics_wiring.svg)

* **Hyperstatic Anti-Bind Float:** The right-hand upper halo joint incorporates a **`±1.5 mm` floating Delrin sleeve** so even if your hand-glued carbon columns have a tiny angle tolerance (`±0.4°`), the columns never bind across the `300 mm` stroke.
* **Slide-Bridge Kitchen Tray:** Dual `MGN9C 300mm` stainless linear rails allow the `6 mm` polycarbonate tray to slide **`300 mm` forward** directly over the kitchen counter or stove while Grandma rests on the raised perch (`713 mm`).
