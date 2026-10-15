> **SUPERSEDED — NOT FOR FABRICATION OR HUMAN USE.** Historical concept only. Use the current root README and hardware/PROTOTYPE_SPEC.md. Claims, costs, dimensions and test counts below are unverified.

# FreeStep (English Edition + ElderStep Pro v2 Improvement Plan)

![FreeStep Open State](Images/FreeStep_open.jpg)

![FreeStep Closed State](Images/FreeStep_close.jpg)

* **Original Video Reference:** [We Built This to Help a Fan Walk... (Bilibili BV17TEC6AE3Z)](https://www.bilibili.com/video/BV17TEC6AE3Z/) / [YouTube Short](https://www.youtube.com/shorts/ZaVE_tBP3jA)
* **Engineering Teardown & Next-Gen Elderly Mobility Improvement Plan:** See **[`IMPROVEMENT_PLAN.md`](IMPROVEMENT_PLAN.md)**
* **Reference ESP32 Safety & Actuator Control Firmware:** See **[`firmware/elderstep_controller/elderstep_controller.ino`](firmware/elderstep_controller/elderstep_controller.ino)**
* **3D CAD Assembly (100% Translated to English Component Tree):** **[`Models/FreeStep.step`](Models/FreeStep.step)**

---

## Safety & Manufacturing Notice

Due to variations in manufacturing processes, materials, equipment, and assembly methods, finished builds will inevitably differ from the reference model.

Please conduct comprehensive safety and durability testing to ensure the device is structurally sound, functional, and stable before any real-world use.

> **WARNING:** Always prioritize physical safety during debugging, testing, and operation. For elderly users or post-surgical rehabilitation (such as ankle fracture recovery), review the structural flaws and upgrades documented in **[`IMPROVEMENT_PLAN.md`](IMPROVEMENT_PLAN.md)** before building.

---

## Complete Bill of Materials (Translated to English)

| Part Name (English) | Original CAD / Reference Name | Qty | Material | Notes & Machining Requirements |
| :--- | :--- | :-: | :--- | :--- |
| Upper Crossbar Bent Tube | `Upper_Crossbar_Bent_Tube` (`上横梁弯管`) | 1 | Aluminum 6061 | Wall thickness: `3.5 mm` |
| Carbon Tube `ø10 × 520 mm` | `Carbon_Tube_10_520` (`碳管-ø10-520`) | 6 | Carbon Fiber | Wall thickness: `2.0 mm` (Linear guide rods) |
| Carbon Tube `ø15 × 560 mm` (3-Hole) | `Carbon_Tube_Dia_15_560_3Hole` (`碳管ø15-560-3孔`) | 2 | Carbon Fiber | Wall thickness: `2.5 mm` |
| Carbon Tube `ø15 × 560 mm` (5-Hole) | `Carbon_Tube_Dia_15_560_5Hole` (`碳管ø15-560-5孔`) | 2 | Carbon Fiber | Wall thickness: `2.5 mm` |
| Carbon Tube `ø30 × 770 mm` (Drilled) | `Carbon_Tube_30_770_Drilled` (`碳管-30-770-打孔`) | 2 | Carbon Fiber | Wall thickness: `3.0 mm` (Lower side rails) |
| Carbon Tube `ø30 × 555 mm` | `Carbon_Tube_Dia_30_555` (`碳管ø30-555`) | 1 | Carbon Fiber | Wall thickness: `3.0 mm` (Lower rear axle beam) |
| Lower Crossbar Joint - Derived (Right) | `Lower_Crossbar_Joint_Derived_Right` (`下横梁连接-衍生-右`) | 1 | Aluminum 6061 | CNC machined |
| Lower Crossbar Joint - Derived (Left) | `Lower_Crossbar_Joint_Derived_Left` (`下横梁连接-衍生-左`) | 1 | Aluminum 6061 | CNC machined |
| Electric Linear Actuator (`SXTL`, `200 mm` Stroke) | `SXTL_Stroke_200` (`SXTL(行程200)`) | 2 | Commercial Assembly | `200 mm` stroke length |
| Side-Mount Shaft Support (`CLTB10`) | `CLTB10` | 4 | Aluminum | Side-mount aluminum clamp (`CLTAM / RCJ07-D10`) |
| Support Carbon Tube Wire Clip | `Support_Carbon_Tube_Wire_Clip` (`支撑碳管线卡`) | 2 | ABS (3D Printed) | |
| Support Carbon Tube Wire Clip (Short) | `Support_Carbon_Tube_Wire_Clip_Short` (`支撑碳管线卡-短`) | 2 | ABS (3D Printed) | |
| Electronics Enclosure Crossbar Wire Clip | `Electronics_Crossbar_Wire_Clip` (`电器仓横梁线卡`) | 2 | ABS (3D Printed) | |
| Motor Wiring Cover Plate | `Motor_Wiring_Cover` (`电机接线盖板`) | 2 | ABS (3D Printed) | |
| LED Strip Holder | `LED_Strip_Holder` (`灯带固定`) | 1 | Clear Photopolymer Resin | SLA 3D printed |
| LED Strip Holder (Mirror) | `LED_Strip_Holder_Mirror` (`灯带固定（镜像）`) | 1 | Clear Photopolymer Resin | SLA 3D printed |
| Lower Crossbar - Front | `Lower_Crossbar_Front` (`下横梁-前`) | 1 | ABS (3D Printed) | Multi-color print (Yellow, White, Blue) |
| Lower Crossbar - Front (Mirror) | `Lower_Crossbar_Front_Mirror` (`下横梁-前(镜像)`) | 1 | ABS (3D Printed) | Multi-color print (Yellow, White, Blue) |
| Shaft Holder Riser Block | `Shaft_Riser_Block` (`轴座垫高块`) | 4 | ABS (3D Printed) | |
| Plate Wheel Tube Clamp | `Plate_Wheel_Tube_Clamp` (`板材轮管夹`) | 2 | ABS (3D Printed) | |
| Linear Shaft Holder - Bottom Right | `Linear_Shaft_Holder_Right_Lower` (`光轴座-右-下`) | 1 | ABS (3D Printed) | |
| Linear Shaft Holder - Bottom Right (Mirror) | `Linear_Shaft_Holder_Right_Lower_Mirror` (`光轴座-右-下(镜像)`) | 1 | ABS (3D Printed) | |
| Linear Actuator Mount Tube Clamp | `Linear_Actuator_Tube_Clamp` (`电推杆固定座管夹`) | 2 | ABS (3D Printed) | |
| Linear Actuator Mount Tube Clamp (Mirror) | `Linear_Actuator_Tube_Clamp_Mirror` (`电推杆固定座管夹（镜像）`) | 2 | ABS (3D Printed) | |
| Lower Crossbar - Rear | `Lower_Crossbar_Rear` (`下横梁-后`) | 1 | ABS (3D Printed) | Consists of 4 internal solid bodies; print separately and assemble |
| Lower Crossbar - Rear (Mirror) | `Lower_Crossbar_Rear_Mirror` (`下横梁-后(镜像)`) | 1 | ABS (3D Printed) | Consists of 4 internal solid bodies; print separately and assemble |
| Hub Motor Tube Clamp | `Hub_Motor_Tube_Clamp` (`轮毂电机管夹`) | 2 | ABS (3D Printed) | |
| Upper Crossbar - Front | `Crossbar_Front` (`横梁-前`) | 1 | ABS (3D Printed) | Multi-color print (Yellow, Red, Blue) |
| Upper Crossbar - Front (Mirror) | `Crossbar_Front_Mirror` (`横梁-前（镜像）`) | 1 | ABS (3D Printed) | Multi-color print (Yellow, Red, Blue) |
| Handle Grip | `Handle_Grip` (`手柄`) | 2 | ABS (3D Printed) | Multi-color print (Yellow, Blue) |
| Cable Routing Baffle - Front | `Cable_Routing_Baffle_Front` (`走线挡板-前`) | 1 | ABS (3D Printed) | |
| Cable Routing Baffle - Front (Mirror) | `Cable_Routing_Baffle_Front_Mirror` (`走线挡板-前（镜像）`) | 1 | ABS (3D Printed) | |
| Upper Crossbar - Rear | `Crossbar_Rear` (`横梁-后`) | 1 | ABS (3D Printed) | |
| Upper Crossbar - Rear (Mirror) | `Crossbar_Rear_Mirror` (`横梁-后（镜像）`) | 1 | ABS (3D Printed) | |
| Wheel Mount Plate | `Wheel_Mount_Plate` (`轮座-板材`) | 4 | Aluminum 6061 | Requires tapped threads |
| Hub Motor Plate 1 | `Hub_Motor_Plate_1` (`轮毂电机-板材1`) | 2 | Aluminum 6061 | |
| Hub Motor Plate 2 | `Hub_Motor_Plate_2` (`轮毂电机-板材2`) | 2 | Aluminum 6061 | Requires tapped threads |
| Wheel Axle | `Wheel_Axle` (`轮轴`) | 2 | 316 Stainless Steel | Requires internal tapped hole + `10 mm` external thread on narrow end |
| Linear Actuator Mount - Carbon Plate | `Linear_Actuator_Mount_Carbon_Plate` (`电推杆固定座-碳板`) | 3 | Carbon Fiber Plate | CNC cut |
| Lower Slider Block | `Lower_Slider` (`下滑块`) | 4 | Aluminum 6061 | Requires tapped threads |
| Linear Ball Bearing (`LM10UU`) | `LM10UU` | 8 | Bearing Steel | `10 mm` bore linear bushing |
| 6-Inch Rubber Wheel | `6_in_Rubber_Wheel` (`6寸橡胶轮`) | 2 | Rubber / Hub | Bore diameter: `ø8 mm` (Front steered wheels) |
| 7-Inch Rubber Wheel | `7_in_Rubber_Wheel` (`7寸橡胶轮`) | 4 | Rubber / Hub | Bore diameter: `ø8 mm` (Rear drive bogie wheels) |
| 12V 550 DC Motor Gearbox | `12v550_Motor_Gearbox` (`12v550电机齿轮箱`) | 2 | Commercial Assembly | Rear drive gearboxes |
| Wheel Hub Adapter | `Wheel_Hub_Adapter` (`轮子转接`) | 2 | Aluminum 6061 | Match spline/plum-blossom coupling to actual gearbox output shaft |
| Upper Linear Bearing Housing | `Linear_Bearing_Block_Upper` (`直线轴承座-上`) | 4 | Aluminum 6061 | Requires tapped threads |
| Timing Belt Clamp Plate | `Timing_Belt_Clamp` (`同步带压板`) | 4 | Aluminum / Steel | `3M` pitch |
| `3M-1188` Timing Belt | `3m-1188` (`3m-1188同步带`) | 2 | Neoprene / Fiberglass | `3 mm` pitch, `1188 mm` perimeter |
| Side Panel - Left | `Side_Panel_Left` (`侧板-左`) | 1 | Carbon Fiber Plate | Electronics / seat box left panel |
| Side Panel - Right | `Side_Panel_Right` (`侧板-右`) | 1 | Carbon Fiber Plate | Electronics / seat box right panel |
| Front Panel | `Front_Panel` (`前面板`) | 1 | Carbon Fiber Plate | Electronics / seat box front panel |
| Linear Shaft Holder (Front Joined Assembly) | `Linear_Shaft_Holder_Aluminum_Joined_Front` (`光轴座 铝拼接-前`) | 1 | Aluminum 6061 | Contains 8 CNC-machined sub-parts; requires tapped threads |
| Linear Shaft Mount | `Linear_Shaft_Mount` (`光轴固定座`) | 1 | Aluminum 6061 | Requires tapped threads |
| Support Carbon Tube Mount | `Support_Carbon_Tube_Mount` (`支撑碳管固定座`) | 1 | Aluminum 6061 | Requires tapped threads |
| Linear Shaft Mount (Mirror) | `Linear_Shaft_Mount_Mirror` (`光轴固定座（镜像）`) | 1 | Aluminum 6061 | Requires tapped threads |
| Support Carbon Tube Mount (Mirror) | `Support_Carbon_Tube_Mount_Mirror` (`支撑碳管固定座（镜像）`) | 1 | Aluminum 6061 | Requires tapped threads |
| Cable Routing Cover | `Cable_Routing_Cover` (`走线盖板`) | 1 | ABS (3D Printed) | |
| Cable Routing Cover (Mirror) | `Cable_Routing_Cover_Mirror` (`走线盖板（镜像）`) | 1 | ABS (3D Printed) | |
| Servo Mount | `Servo_Mount` (`舵机座`) | 1 | Aluminum 6061 | Requires tapped threads |
| Servo Mount (Mirror) | `Servo_Mount_Mirror` (`舵机座（镜像）`) | 1 | Aluminum 6061 | Requires tapped threads |
| Feetech Serial Bus Servo (`ST-3032-C001`) | `Feetech_Servo_ST-3032-C001` (`飞特舵机-ST-3032-C001`) | 2 | Commercial Servo | Use with original metal servo horn (`舵盘`) |
| `3M` Timing Pulley (25-Tooth) | `3M_Timing_Pulley-25` (`3M同步轮-25`) | 4 | Aluminum | `3 mm` pitch, 25 teeth |
| Large Spur Gear | `Large_Spur_Gear` (`大齿轮`) | 2 | Carbon Fiber Plate | Requires `M4` countersunk holes (Front steering gear) |
| Silicone Snap-In Sealing Plug | `Silicone_Sealing_Plug` (`硅胶倒扣密封孔塞`) | 4 | Silicone | Allow extra spares for installation wear |
| Nyloc Locknut `M8` | `Nyloc_Locknut-M8` (`防松螺母-M8`) | 2 | Steel | |
| Nyloc Locknut `M6` | `Nyloc_Locknut-M6` (`防松螺母-M6`) | 10 | Steel | |
| Nyloc Locknut `M5` | `Nyloc_Locknut-M5` (`防松螺母-M5`) | 16 | Steel | |
| Nyloc Locknut `M4` | `Nyloc_Locknut-M4` (`防松螺母-M4`) | 20 | Steel | |
| Custom PTFE Saddle Washers (Duckbill Spacers) | `Custom_PTFE_Saddle_Washer` (`定制特氟龙鸭嘴垫片`) | As req. | PTFE (Teflon) | Adjust thickness as needed for tube tolerances |
| Hex Socket Sex Bolt / Binding Screw `ø6 × 45 mm` | `Sex_Bolt_6x45` (`内六角-对锁螺丝-ø6x45`) | 4 | Steel | |
| Dacromet Flat Washer `M8` | `Dacromet_Washer-M8` (`达克罗垫片-M8`) | 10 | Dacromet Steel | |
| Hex Socket Shoulder Bolt `ø8 × 20 mm` | `Hex_Socket-Shoulder_Bolt-Dia_8x20` (`内六角-轴肩-ø8x20`) | 4 | Alloy Steel | `8 mm` shoulder diameter, `20 mm` shoulder length |
| Hex Socket Shoulder Bolt `ø8 × 35 mm` | `Hex_Socket-Shoulder_Bolt-Dia_8x35` (`内六角-轴肩-ø8x35`) | 4 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø8 × 40 mm` | `Hex_Socket-Shoulder_Bolt-Dia_8x40` (`内六角-轴肩-ø8x40`) | 2 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø8 × 45 mm` | `Hex_Socket-Shoulder_Bolt-Dia_8x45` (`内六角-轴肩-ø8x45`) | 2 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø8 × 60 mm` | `Hex_Socket-Shoulder_Bolt-Dia_8x60` (`内六角-轴肩-ø8x60`) | 2 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø6 × 16 mm` | `Hex_Socket-Shoulder_Bolt-Dia_6x16` (`内六角-轴肩-ø6x16`) | 4 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø6 × 20 mm` | `Hex_Socket-Shoulder_Bolt-Dia_6x20` (`内六角-轴肩-ø6x20`) | 6 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø6 × 22 mm` | `Hex_Socket-Shoulder_Bolt-Dia_6x22` (`内六角-轴肩-ø6x22`) | 2 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø6 × 25 mm` | `Hex_Socket-Shoulder_Bolt-Dia_6x25` (`内六角-轴肩-ø6x25`) | 4 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø6 × 40 mm` | `Hex_Socket-Shoulder_Bolt-Dia_6x40` (`内六角-轴肩-ø6x40`) | 4 | Alloy Steel | |
| Hex Socket Shoulder Bolt `ø6 × 55 mm` | `Hex_Socket-Shoulder_Bolt-Dia_6x55` (`内六角-轴肩-ø6x55`) | 4 | Alloy Steel | |
| Socket Head Cap Screw `M2 × 4 mm` | `Hex_Socket-Socket_Head_Cap-M2x4` (`内六角-杯头-M2x4`) | 8 | Steel | |
| Socket Head Cap Screw `M2 × 5 mm` | `Hex_Socket-Socket_Head_Cap-M2x5` (`内六角-杯头-M2x5`) | 20 | Steel | |
| Socket Head Cap Screw `M2 × 8 mm` | `Hex_Socket-Socket_Head_Cap-M2x8` (`内六角-杯头-M2x8`) | 16 | Steel | |
| Socket Head Cap Screw `M3 × 10 mm` | `Hex_Socket-Socket_Head_Cap-M3x10` (`内六角-杯头-M3x10`) | 20 | Steel | |
| Socket Head Cap Screw `M3 × 14 mm` | `Hex_Socket-Socket_Head_Cap-M3x14` (`内六角-杯头-M3x14`) | 8 | Steel | |
| Socket Head Cap Screw `M3 × 16 mm` | `Hex_Socket-Socket_Head_Cap-M3x16` (`内六角-杯头-M3x16`) | 16 | Steel | |
| Socket Head Cap Screw `M4 × 10 mm` | `Hex_Socket-Socket_Head_Cap-M4x10` (`内六角-杯头-M4x10`) | 8 | Steel | |
| Socket Head Cap Screw `M4 × 12 mm` | `Hex_Socket-Socket_Head_Cap-M4x12` (`内六角-杯头-M4x12`) | 20 | Steel | |
| Socket Head Cap Screw `M4 × 18 mm` | `Hex_Socket-Socket_Head_Cap-M4x18` (`内六角-杯头-M4x18`) | 8 | Steel | |
| Socket Head Cap Screw `M4 × 45 mm` | `Hex_Socket-Socket_Head_Cap-M4x45` (`内六角-杯头-M4x45`) | 16 | Steel | |
| Socket Head Cap Screw `M5 × 45 mm` | `Hex_Socket-Socket_Head_Cap-M5x45` (`内六角-杯头-M5x45`) | 10 | Steel | |
| Socket Head Cap Screw `M6 × 65 mm` | `Hex_Socket-Socket_Head_Cap-M6x65` (`内六角-杯头-M6x65`) | 10 | Steel | |
| Socket Head Cap Screw `M8 × 65 mm` | `Hex_Socket-Socket_Head_Cap-M8x65` (`内六角-杯头-M8x65`) | 10 | Steel | |
| Hex Socket Flat-Tail Self-Tapping Screw `M2 × 12 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M2x12` (`内六角-平尾自攻-M2x12`) | 10 | Steel | |
| Hex Socket Flat-Tail Self-Tapping Screw `M2 × 18 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M2x18` (`内六角-平尾自攻-M2x18`) | 10 | Steel | |
| Hex Socket Flat-Tail Self-Tapping Screw `M2 × 20 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M2x20` (`内六角-平尾自攻-M2x20`) | 10 | Steel | |
| Hex Socket Flat-Tail Self-Tapping Screw `M2 × 25 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M2x25` (`内六角-平尾自攻-M2x25`) | 8 | Steel | |
| Hex Socket Flat-Tail Self-Tapping Screw `M3 × 8 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M3x8` (`内六角-平尾自攻-M3x8`) | 8 | Steel | |
| Hex Socket Flat-Tail Self-Tapping Screw `M3 × 15 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M3x15` (`内六角-平尾自攻-M3x15`) | 16 | Steel | Listed as two rows of 8 in original BOM |
| Hex Socket Flat-Tail Self-Tapping Screw `M4 × 20 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M4x20` (`内六角-平尾自攻-M4x20`) | 8 | Steel | |
| Hex Socket Flat-Tail Self-Tapping Screw `M4 × 30 mm` | `Hex_Socket-Flat_Tail_Self_Tapping-M4x30` (`内六角-平尾自攻-M4x30`) | 10 | Steel | |
| Countersunk Hex Socket Screw `M4 × 16 mm` | `Hex_Socket-Countersunk-M4x16` (`内六角-沉头-M4x16`) | 8 | Steel | |

> **Assembly Note 1:** Apply threadlocker (e.g., Loctite 243) to all machine screws and threaded fastener joints.
>
> **Assembly Note 2:** Tapped hole color/diameter recognition rules in the STEP file follow standard CNC sheet/machining thread-identification conventions.
