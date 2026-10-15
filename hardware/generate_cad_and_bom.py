#!/usr/bin/env python3
"""
ElderStep Pro (Final 10.20 kg 5-Module Carbon/7075 Edition) - CAD, Cutlist & BOM Generator
Incorporates Global Benchmark Refinements (MIT E-BAR, Rifton TRAM, RT.Works RT.2, Camino, SkyWalker):
  1. 12-Degree Forward-Inclined "Nose-Over-Toes" Lifting Column Mounts (+293mm UP, +62mm FORWARD)
  2. 75mm (3-inch) Low-Profile "Slide-Under-Bed" Front Nose Rails (slides under Indian beds/sofas)
  3. Fixed 495mm (19.5-inch) Bathroom-Ready U-Base (zero width-morphing actuator bloat)
  4. Bi-Level Sit-to-Stand Push Grips + MIT E-BAR Lateral Waist Bolster Mounts
  5. Passive Insulated Silicone Cup Well + 1-Hand Mechanical Ratchet Calf Rest
"""

import csv
import math
import os


def ensure_dirs():
    os.makedirs("hardware/cnc_7075", exist_ok=True)
    os.makedirs("hardware/laser_cut", exist_ok=True)
    os.makedirs("hardware/3d_print", exist_ok=True)


def write_dxf(filepath, polylines, circles):
    lines = [
        "0", "SECTION",
        "2", "HEADER",
        "9", "$INSUNITS", "70", "4",  # 4 = Millimeters
        "0", "ENDSEC",
        "0", "SECTION",
        "2", "ENTITIES"
    ]
    for poly in polylines:
        for i in range(len(poly)):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % len(poly)]
            lines.extend([
                "0", "LINE",
                "8", "CNC_PROFILE",
                "10", f"{x1:.4f}",
                "20", f"{y1:.4f}",
                "30", "0.0",
                "11", f"{x2:.4f}",
                "21", f"{y2:.4f}",
                "31", "0.0"
            ])
    for cx, cy, r in circles:
        lines.extend([
            "0", "CIRCLE",
            "8", "CNC_BORES",
            "10", f"{cx:.4f}",
            "20", f"{cy:.4f}",
            "30", "0.0",
            "40", f"{r:.4f}"
        ])
    lines.extend(["0", "ENDSEC", "0", "EOF"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_svg(filepath, width_mm, height_mm, polylines, circles, title):
    margin = 12.0
    vw = width_mm + 2 * margin
    vh = height_mm + 2 * margin
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{vw}mm" height="{vh}mm" viewBox="{-margin} {-margin} {vw} {vh}">',
        f'  <title>{title}</title>',
        '  <g fill="none" stroke="#0055ff" stroke-width="0.5">',
    ]
    for poly in polylines:
        pts = " ".join(f"{x:.3f},{height_mm - y:.3f}" for x, y in poly)
        svg.append(f'    <polygon points="{pts}" />')
    svg.append('  </g>')
    svg.append('  <g fill="none" stroke="#e60000" stroke-width="0.4">')
    for cx, cy, r in circles:
        svg.append(f'    <circle cx="{cx:.3f}" cy="{height_mm - cy:.3f}" r="{r:.3f}" />')
    svg.append('  </g>')
    svg.append('</svg>')
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(svg) + "\n")


def box_triangles(x0, y0, z0, x1, y1, z1):
    v = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)
    ]
    faces = [
        (0, 2, 1), (0, 3, 2),
        (4, 5, 6), (4, 6, 7),
        (0, 1, 5), (0, 5, 4),
        (2, 3, 7), (2, 7, 6),
        (0, 4, 7), (0, 7, 3),
        (1, 2, 6), (1, 6, 5),
    ]
    return [(v[a], v[b], v[c]) for a, b, c in faces]


def write_ascii_stl(filepath, name, triangles):
    lines = [f"solid {name}"]
    for p1, p2, p3 in triangles:
        ux, uy, uz = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
        vx, vy, vz = p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]
        nx = uy * vz - uz * vy
        ny = uz * vx - ux * vz
        nz = ux * vy - uy * vx
        length = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
        nx, ny, nz = nx / length, ny / length, nz / length
        lines.append(f"  facet normal {nx:.4f} {ny:.4f} {nz:.4f}")
        lines.append("    outer loop")
        lines.append(f"      vertex {p1[0]:.4f} {p1[1]:.4f} {p1[2]:.4f}")
        lines.append(f"      vertex {p2[0]:.4f} {p2[1]:.4f} {p2[2]:.4f}")
        lines.append(f"      vertex {p3[0]:.4f} {p3[1]:.4f} {p3[2]:.4f}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {name}")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def generate_cnc_7075_parts():
    # 1. 12-Degree Forward-Inclined Lifting Column Base Gusset ("Nose-Over-Toes" Sit-to-Stand Mount)
    # Tilts the TiMOTION TL18 / LINAK LC1 telescoping column 12 deg forward so 300mm stroke = +293mm UP & +62mm FORWARD
    incline_poly = [
        (0.0, 0.0), (145.0, 0.0), (145.0, 38.0),
        (115.0, 125.0), (22.0, 105.0), (0.0, 38.0)
    ]
    incline_circles = [
        (25.0, 18.0, 4.1), (72.0, 18.0, 4.1), (120.0, 18.0, 4.1),  # 3x M8 Base Rail Bolts
        (45.0, 75.0, 3.2), (95.0, 86.0, 3.2),                      # 12-deg tilted M6 Column Base Plate Mounts
    ]
    write_dxf("hardware/cnc_7075/inclined_12deg_column_mount.dxf", [incline_poly], incline_circles)
    write_svg("hardware/cnc_7075/inclined_12deg_column_mount.svg", 145.0, 125.0, [incline_poly], incline_circles,
              "CNC 7075-T6 12-Deg Forward-Inclined Column Mount (Nose-Over-Toes)")
    incline_tris = box_triangles(0, 0, 0, 145, 125, 16)
    write_ascii_stl("hardware/cnc_7075/inclined_12deg_column_mount.stl", "inclined_12deg_column_mount", incline_tris)

    # 2. Low-Profile 75mm (3-inch) "Slide-Under-Bed" Step-Down Front Nose Rail (Inspired by Rifton TRAM)
    # Steps the front 220mm of the side rail down so total height with 65mm twin-caster is <= 75mm (slides under any bed/sofa)
    nose_poly = [
        (0.0, 25.0), (110.0, 25.0), (160.0, 0.0), (340.0, 0.0),
        (340.0, 28.0), (170.0, 28.0), (120.0, 58.0), (0.0, 58.0)
    ]
    nose_circles = [
        (25.0, 41.5, 4.1), (85.0, 41.5, 4.1),    # Rear M8 splice to main lower carbon rail
        (210.0, 14.0, 4.1), (310.0, 14.0, 4.1),  # Recessed low-profile Tente twin-caster mount
    ]
    write_dxf("hardware/cnc_7075/low_profile_75mm_bed_nose_rail.dxf", [nose_poly], nose_circles)
    write_svg("hardware/cnc_7075/low_profile_75mm_bed_nose_rail.svg", 340.0, 58.0, [nose_poly], nose_circles,
              "CNC 7075-T6 75mm Slide-Under-Bed Front Nose Rail")
    nose_tris = box_triangles(0, 25, 0, 120, 58, 14) + box_triangles(120, 0, 0, 340, 28, 14)
    write_ascii_stl("hardware/cnc_7075/low_profile_75mm_bed_nose_rail.stl", "low_profile_75mm_bed_nose_rail", nose_tris)

    # 3. Fidlock Auto-Latching 180-Deg Split-Saddle Hinge Block (7075-T6 Billet)
    saddle_poly = [
        (0.0, 0.0), (105.0, 0.0), (130.0, 22.0),
        (130.0, 68.0), (105.0, 90.0), (0.0, 90.0)
    ]
    saddle_circles = [
        (26.0, 45.0, 12.6),  # Telescoping column clamp bore
        (100.0, 45.0, 5.0),  # Ø10mm shoulder-bolt thrust-bearing saddle pivot
        (68.0, 45.0, 4.0),   # Fidlock magnetic-mechanical plunger lock (90-deg seated/perch)
        (100.0, 77.0, 4.0),  # Fidlock magnetic-mechanical plunger lock (0-deg open walking)
    ]
    write_dxf("hardware/cnc_7075/fidlock_split_saddle_hinge.dxf", [saddle_poly], saddle_circles)
    write_svg("hardware/cnc_7075/fidlock_split_saddle_hinge.svg", 130.0, 90.0, [saddle_poly], saddle_circles,
              "CNC 7075-T6 Fidlock Split-Saddle Hinge")
    saddle_tris = box_triangles(0, 0, 0, 55, 90, 32) + box_triangles(55, 15, 6, 130, 75, 26)
    write_ascii_stl("hardware/cnc_7075/fidlock_split_saddle_hinge.stl", "fidlock_split_saddle_hinge", saddle_tris)

    # 4. Rear ZLTECH Servo Hub Motor Dropout + VL53L1X Cliff & VL53L5CX Shin-Tracker Mount (7075-T6 Billet)
    dropout_poly = [
        (0.0, 0.0), (115.0, 0.0), (115.0, 65.0),
        (75.0, 95.0), (0.0, 95.0)
    ]
    dropout_circles = [
        (25.0, 70.0, 15.1),  # Ø30mm lower carbon side-rail bore
        (80.0, 32.0, 6.0),   # Ø12mm anti-rotation ZLTECH servo hub motor axle slot
        (25.0, 22.0, 3.1),   # M6 VL53L1X rear step-drop ToF & VL53L5CX shin-tracker mount
    ]
    write_dxf("hardware/cnc_7075/foc_hub_motor_dropout.dxf", [dropout_poly], dropout_circles)
    write_svg("hardware/cnc_7075/foc_hub_motor_dropout.svg", 115.0, 95.0, [dropout_poly], dropout_circles,
              "CNC 7075-T6 Rear Servo Hub Dropout + Shin/Cliff ToF Mount")
    dropout_tris = box_triangles(0, 0, 0, 115, 95, 16)
    write_ascii_stl("hardware/cnc_7075/foc_hub_motor_dropout.stl", "foc_hub_motor_dropout", dropout_tris)


def generate_3d_print_stls():
    # 1. Bi-Level Forearm Load-Cell Cockpit + Lower Sit-to-Stand Push Grip (Waterloo SkyWalker + MIT E-BAR)
    tris = []
    tris.extend(box_triangles(0, 0, 0, 190, 95, 8))          # Load-cell flexure base plate
    tris.extend(box_triangles(0, 0, 8, 190, 10, 36))         # Left ergonomic forearm lip
    tris.extend(box_triangles(0, 85, 8, 190, 95, 36))        # Right ergonomic forearm lip
    tris.extend(box_triangles(190, 15, 0, 240, 80, 32))      # Sealed switch & OLED status pod
    tris.extend(box_triangles(20, 30, -145, 140, 65, -115))  # Lower bi-level Sit-to-Stand push handle (-145mm below forearm)
    write_ascii_stl("hardware/3d_print/forearm_loadcell_cockpit.stl", "forearm_loadcell_cockpit", tris)

    # 2. Boa-Dial Orthopedic "Air-Float" Ankle Cradle Shell
    cradle_tris = []
    cradle_tris.extend(box_triangles(0, 0, 0, 220, 115, 8))
    cradle_tris.extend(box_triangles(0, 0, 8, 220, 12, 48))
    cradle_tris.extend(box_triangles(0, 103, 8, 220, 115, 48))
    cradle_tris.extend(box_triangles(0, 30, -28, 48, 85, 0))
    write_ascii_stl("hardware/3d_print/boa_ankle_cradle_shell.stl", "boa_ankle_cradle_shell", cradle_tris)


def generate_universal_cutlist_csv():
    rows = [
        ["Part ID", "Component / Tube Name", "Material & Spec", "Outer Dia / Profile (mm)", "Wall (mm)", "Exact Cut Length (mm)", "Qty", "Target Subsystem & Notes"],
        ["CF-01", "Rear Lower Chassis Tubes (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø30.0", "2.5", "420.0", 2, "Connects rear ZLTECH hub dropouts to 75mm low-profile under-bed front nose rails"],
        ["CF-02", "Fixed 495mm Front Lower Cross-Beam", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø30.0", "3.0", "435.0", 1, "Sets outer frame width to 495mm (19.5in) -> clears every 20in+ Indian bathroom door"],
        ["CF-03", "Fixed 495mm Front Upper Cockpit Bridge", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø25.0", "2.5", "435.0", 1, "Links tops of left & right TiMOTION/LINAK columns; carries Slide-Bridge Kitchen Tray"],
        ["CF-04", "Upper Forearm Cockpit & Waist Bolster Tubes (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø25.0", "2.5", "420.0", 2, "Supports 24-bit Load-Cell Forearm Troughs, Bi-Level Rise Grips & MIT E-BAR Waist Bolsters"],
        ["CF-05", "Split-Saddle Cantilever Arms (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø25.0", "3.0", "230.0", 2, "Pivots 90-deg on Fidlock 7075-T6 Hinge Block behind user's pelvis"],
        ["LK-01", "12-Deg Inclined Telescoping Medical Columns", "TiMOTION TL18 / LINAK LC1 Factory Column", "Anodized Extruded Al", "IPX6", "300.0 Stroke (440mm Retracted)", 2, "Mounted at 12-deg forward incline (+293mm UP & +62mm FORWARD nose-over-toes trajectory)"],
    ]
    with open("hardware/CARBON_TUBE_CUTLIST.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def generate_final_bom_csv():
    rows = [
        ["Batch", "Module", "Item Name", "Final No-Compromise Specification", "Mass (kg)", "Qty", "India Supplier & Contact", "Lead Time", "Total Price (INR)"],
        ["Batch 1 (Day 1)", "Module 1: Lift", "Factory Telescoping Medical Lifting Columns", "TiMOTION TL18 / LINAK LC1 (24V, 1500N each, 300mm stroke, <42dB, IPX6, Hall Sync)", "2.40", "2", "Linak India (Bengaluru/Mumbai) / TiMOTION India", "7-10 Days", "18500"],
        ["Batch 1 (Day 1)", "Module 3: Drive", "6.5-inch Integrated Robotics Servo Hub Wheels", "ZLTECH ZLLG65ASM200 (24V FOC closed-loop, 4096-PPR encoder + E-brake + RS485/PWM Driver)", "1.80", "2", "Robu.in / IndiaMART AMR Suppliers", "5-7 Days", "13500"],
        ["Batch 2 (Day 2)", "Module 2: CNC", "CNC 7075-T6 Billet Plates & Fidlock Hinges", "12-deg Column Mounts, 75mm Under-Bed Nose Rails, Split-Saddle Hinges, Hub Dropouts + Ti Bolts", "1.45", "12 pcs", "Karkhana.io / Fracktal Works / Robu CNC", "5-7 Days", "9800"],
        ["Batch 2 (Day 2)", "Module 2: Carbon", "3K Roll-Wrapped Autoclave Carbon Tube Set", "Pre-cut Ø30mm & Ø25mm twill weave tubes (from CARBON_TUBE_CUTLIST.csv) + 3M DP420 Epoxy", "0.95", "1 set", "Robu.in / Composite Hub India", "3-5 Days", "6400"],
        ["Batch 3 (Day 3)", "Module 5: Brain", "ESP32-S3 + 24-Bit Load-Cells + IMU + Shin ToF", "ESP32-S3 + 2x 20kg Load Cells (ADS1220) + MPU6050 (Slope-Zeroing) + VL53L5CX (Camino Shin Guard) + 2x VL53L1X Cliff", "0.25", "1 set", "Robu.in / Evelta Electronics (Mumbai)", "2-3 Days", "4300"],
        ["Batch 3 (Day 3)", "Module 5: Summon", "UWB Dual-Anchor AoA + Wearable Pendant + LiDAR", "2x Makerfabs MaUWB_ESP32S3 (DW3000) + 1x UWB Wrist Tag + LD19 360-Deg DToF LiDAR + INMP441 Mic", "0.15", "1 set", "Robu.in / Evelta Electronics", "2-4 Days", "7400"],
        ["Batch 3 (Day 3)", "Module 5: Power", "Hot-Swap 600g 24V Lithium Pack + Mag Floor Dock", "21700 24V 10Ah Pack + 100W USB-C PD + Magnetic Pogo-Pin Park-and-Charge Floor Mat", "0.75", "1 set", "Robu.in / Local EV Pack Builder", "3-4 Days", "6800"],
        ["Batch 4 (Day 4)", "Module 3: Front", "Low-Profile 65mm Medical Twin-Wheel Casters", "Tente / Blickle 65mm Dual-Roller PU Casters with Foot-Click Straight-Line Directional Lock", "0.45", "2", "Tente India / Blickle India", "3-5 Days", "3800"],
        ["Batch 4 (Day 4)", "Module 4: Cushions", "Viscoelastic Gel Saddle + Waist Bolsters + Cradle", "Dartex waterproof memory-gel Split-Saddle, Fidlock latches, MIT Lateral Waist Bolsters, Boa Ankle Cradle, Ratchet Calf Rest", "1.45", "1 set", "Custom Medical Orthotic Upholstery", "4-6 Days", "5600"],
        ["Batch 4 (Day 4)", "Module 4: Tray", "Slide-Bridge Carbon Kitchen Tray + Cup Well + Qi2", "Recessed insulated silicone anti-slosh cup well + 15W MagSafe/Qi2 charger + 3D-printed Bi-Level Grips", "0.55", "1 set", "Robu 3D Print + CNC Carbon Plate", "3-4 Days", "3100"],
        ["TOTAL", "ALL 5 MODULES", "ElderStep Pro (Final 10.20 kg 5-Module Spec)", "Total Mass: 10.20 kg (22.4 lbs) | Fixed Width: 495mm | 12-Deg Lift: 420-880mm | 75mm Under-Bed Nose", "10.20", "-", "-", "10 Days Total", "79200"],
    ]
    with open("hardware/INDIA_BOM_SOURCING.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == "__main__":
    ensure_dirs()
    generate_cnc_7075_parts()
    generate_3d_print_stls()
    generate_universal_cutlist_csv()
    generate_final_bom_csv()
    print("Generated Final 10.20 kg 5-Module CAD, Cutlist, and Batch Procurement BOM successfully!")
