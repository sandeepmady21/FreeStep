#!/usr/bin/env python3
"""
ElderStep Pro (FreeStep v2) - Parametric CAD & BOM Generator
Generates:
  1. 2D DXF & SVG laser-cutting files (in mm) for 4mm/6mm steel/aluminum brackets:
     - hardware/laser_cut/split_saddle_hinge_bracket.{dxf,svg}
     - hardware/laser_cut/actuator_column_gusset.{dxf,svg}
  2. 3D Binary/ASCII STL files (in mm) for non-structural 3D-printed ergonomic mounts:
     - hardware/3d_print/forearm_cockpit_mount.stl
     - hardware/3d_print/ankle_knee_cradle_clamp.stl
  3. Complete India procurement BOM CSV:
     - hardware/INDIA_BOM_SOURCING.csv
"""

import csv
import math
import os


def ensure_dirs():
    os.makedirs("hardware/laser_cut", exist_ok=True)
    os.makedirs("hardware/3d_print", exist_ok=True)


def write_dxf(filepath, polylines, circles):
    """Writes a standard AutoCAD R12/LT2 DXF file in millimeters for CNC laser cutting."""
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
                "8", "CUT_OUTER",
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
            "8", "CUT_HOLES",
            "10", f"{cx:.4f}",
            "20", f"{cy:.4f}",
            "30", "0.0",
            "40", f"{r:.4f}"
        ])
    lines.extend(["0", "ENDSEC", "0", "EOF"])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def write_svg(filepath, width_mm, height_mm, polylines, circles, title):
    """Writes a 1:1 millimeter-scaled SVG file for inspection and laser cutting."""
    margin = 15.0
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
    svg.append('  <g fill="none" stroke="#ff0000" stroke-width="0.4">')
    for cx, cy, r in circles:
        svg.append(f'    <circle cx="{cx:.3f}" cy="{height_mm - cy:.3f}" r="{r:.3f}" />')
    svg.append('  </g>')
    svg.append('</svg>')
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(svg) + "\n")


def generate_laser_cut_brackets():
    # 1. 180-Degree Split-Saddle Hinge & Inner Column Bracket (6mm 6061 Aluminum / Mild Steel)
    # Clamps onto 35x35mm inner telescoping column and provides a heavy-duty Ø10mm vertical hinge pivot
    # plus 2x Ø8mm lock-pin holes (0 deg Walking Open, 90 deg Seated/Perch Locked)
    outer_poly = [
        (0.0, 0.0),
        (110.0, 0.0),
        (135.0, 25.0),
        (135.0, 65.0),
        (110.0, 90.0),
        (0.0, 90.0)
    ]
    # Holes: (cx, cy, radius_mm)
    holes = [
        # 4x M6 mounting holes for 35x35mm telescoping column face
        (18.0, 18.0, 3.2),
        (52.0, 18.0, 3.2),
        (18.0, 72.0, 3.2),
        (52.0, 72.0, 3.2),
        # Main Ø10mm shoulder-bolt pivot hole for split-saddle wing
        (105.0, 45.0, 5.1),
        # Index plunger lock holes (Seated locked position & Walking folded position) at R=32mm from pivot
        (105.0 - 32.0, 45.0, 4.1),
        (105.0, 45.0 + 32.0, 4.1),
    ]
    write_dxf("hardware/laser_cut/split_saddle_hinge_bracket.dxf", [outer_poly], holes)
    write_svg("hardware/laser_cut/split_saddle_hinge_bracket.svg", 135.0, 90.0, [outer_poly], holes,
              "Split-Saddle Hinge Bracket (6mm Al6061 / Steel)")

    # 2. Vertical Linear Actuator (1500N) & Outer 40x40mm Column Base Gusset (5mm Mild Steel / Al6061)
    gusset_poly = [
        (0.0, 0.0),
        (140.0, 0.0),
        (140.0, 45.0),
        (60.0, 120.0),
        (0.0, 120.0)
    ]
    gusset_holes = [
        # Bottom rail mounting holes (M8)
        (20.0, 20.0, 4.2),
        (65.0, 20.0, 4.2),
        (115.0, 20.0, 4.2),
        # Vertical column mounting holes (M6)
        (20.0, 65.0, 3.2),
        (20.0, 100.0, 3.2),
        # Linear actuator clevis pin hole (Ø8mm / M8 shoulder bolt)
        (95.0, 42.0, 4.1),
    ]
    write_dxf("hardware/laser_cut/actuator_column_gusset.dxf", [gusset_poly], gusset_holes)
    write_svg("hardware/laser_cut/actuator_column_gusset.svg", 140.0, 120.0, [gusset_poly], gusset_holes,
              "Vertical Actuator & Column Base Gusset (5mm Steel)")


def box_triangles(x0, y0, z0, x1, y1, z1):
    """Returns 12 triangles defining an axis-aligned box."""
    v = [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)
    ]
    faces = [
        (0, 2, 1), (0, 3, 2),  # Bottom
        (4, 5, 6), (4, 6, 7),  # Top
        (0, 1, 5), (0, 5, 4),  # Front
        (2, 3, 7), (2, 7, 6),  # Back
        (0, 4, 7), (0, 7, 3),  # Left
        (1, 2, 6), (1, 6, 5),  # Right
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


def generate_3d_print_stls():
    # 1. Forearm Cockpit & FSR Sensor Tray (Non-structural ergonomic cradle + switch box)
    # 180mm long x 95mm wide U-channel with recessed FSR pocket
    tris = []
    tris.extend(box_triangles(0, 0, 0, 180, 95, 6))       # Base plate
    tris.extend(box_triangles(0, 0, 6, 180, 10, 32))      # Left armrest lip
    tris.extend(box_triangles(0, 85, 6, 180, 95, 32))     # Right armrest lip
    tris.extend(box_triangles(180, 15, 0, 225, 80, 28))   # Front switch cockpit housing
    write_ascii_stl("hardware/3d_print/forearm_cockpit_mount.stl", "forearm_cockpit_mount", tris)

    # 2. Modular Ankle-Offload Knee Cradle Clamp Sleeve (slides onto 40x40mm outer column)
    clamp_tris = []
    clamp_tris.extend(box_triangles(0, 0, 0, 52, 6, 60))     # Back wall
    clamp_tris.extend(box_triangles(0, 46, 0, 52, 52, 60))   # Front wall
    clamp_tris.extend(box_triangles(0, 6, 0, 6, 46, 60))     # Left wall
    clamp_tris.extend(box_triangles(46, 6, 0, 52, 46, 60))   # Right wall
    clamp_tris.extend(box_triangles(52, 12, 10, 85, 40, 50)) # Clevis ear for padded knee trough
    write_ascii_stl("hardware/3d_print/ankle_knee_cradle_clamp.stl", "ankle_knee_cradle_clamp", clamp_tris)


def generate_india_bom_csv():
    rows = [
        ["Subsystem", "Item Name", "Specification", "Qty", "Preferred India Source", "Unit Price (INR)", "Total Price (INR)"],
        ["Vertical Lift", "Heavy-Duty Electric Linear Actuator", "24V DC, 1500N (150kgf), 250mm Stroke, IP65, Hall Sensor Feedback", 2, "Robu.in / IndiaMART", 2600, 5200],
        ["Width Morph", "Compact Linear Actuator", "24V DC, 1000N, 130mm Stroke, Built-in Limit Switches", 1, "Robu.in", 1900, 1900],
        ["Width Morph", "Hardened Chrome Linear Shafts + Bearings", "16mm Dia x 650mm SFC16 Shaft (x2) + LMF16LUU Flanged Bearings (x4)", 1, "Robu.in / Local CNC", 1800, 1800],
        ["Chassis", "Telescoping Square Tubes + Wear Pads", "6061-T6 Al / SS304 40x40x2.5mm & 35x35x2.5mm + UHMW-PE Strips", 1, "Local Metal Market / IndiaMART", 2800, 2800],
        ["Brackets", "Laser-Cut Structural Gussets & Saddle Hinges", "5mm/6mm Mild Steel / Al6061 (from hardware/laser_cut/*.dxf)", 12, "Robu Laser Cutting Service", 185, 2220],
        ["Drivetrain", "6.5-inch Geared/Direct BLDC Hub Motor Wheels", "24V 250W High-Torque Hub Motors with Hall Sensors & E-Brake", 2, "IndiaMART / EV Suppliers", 1800, 3600],
        ["Front Casters", "6-inch Heavy-Duty Medical Swivel Casters", "PU Tread, Sealed Precision Ball Bearings, 360-Deg Swivel", 2, "Kosmochem / IndiaMART", 550, 1100],
        ["Electronics", "ESP32-S3 DevKitC-1 + MPU6050 6-Axis IMU", "Dual-Core MCU + I2C Accelerometer/Gyroscope for Stumble Lock", 1, "Robu.in", 650, 650],
        ["Motor Drivers", "BTS7960 43A H-Bridge Drivers + ZS-X11H BLDC Drivers", "3x BTS7960 (Actuators) + 2x ZS-X11H (Rear Hub Motors)", 1, "Robu.in", 1750, 1750],
        ["Sensors & UI", "Forearm FSR402 Force Sensors + Waterproof Rockers", "2x FSR402 + 3x IP65 Momentary Rocker Switches + 2x Limit Switches", 1, "Robu.in", 950, 950],
        ["Power System", "24V 8Ah LiFePO4 Battery Pack + BMS + Charger", "Lightweight Lithium Iron Phosphate Pack + Emergency Stop Switch", 1, "Robu.in / Local EV Pack Builder", 3200, 3200],
        ["Ergonomics", "Padded Forearm Troughs + Split Saddle + Knee Cradle", "High-Density Memory Foam + Wipeable Medical Vinyl + Tray", 1, "Local Upholstery / KosmoCare", 1800, 1800],
        ["3D Prints", "Non-Structural Sensor Covers & Switch Cockpit", "PETG/ABS Filament (~600g, from hardware/3d_print/*.stl)", 1, "Self / Robu 3D Printing", 650, 650],
    ]
    with open("hardware/INDIA_BOM_SOURCING.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == "__main__":
    ensure_dirs();
    generate_laser_cut_brackets()
    generate_3d_print_stls()
    generate_india_bom_csv()
    print("Generated DXF, SVG, STL, and CSV BOM files in hardware/ successfully!")
