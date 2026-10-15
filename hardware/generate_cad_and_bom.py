#!/usr/bin/env python3
"""
ElderStep Pro (Universal Home & Hospital Carbon/7075 Edition) - CAD & Cutlist Generator
Generates:
  1. 5-Axis / 3-Axis CNC 7075-T6 Billet Aluminum Part Models (STL + DXF + SVG):
     - hardware/cnc_7075/od30_split_clamp_lug.{stl,dxf,svg}
     - hardware/cnc_7075/igus_drylin_width_carriage_mount.{stl,dxf,svg}
     - hardware/cnc_7075/fidlock_split_saddle_hinge.{stl,dxf,svg}
     - hardware/cnc_7075/foc_hub_motor_dropout.{stl,dxf,svg}
  2. 3D-Printed Medical Ergonomic Cockpit & Orthopedic Mounts (STL):
     - hardware/3d_print/forearm_loadcell_cockpit.stl
     - hardware/3d_print/boa_ankle_cradle_shell.stl
  3. Universal Carbon Tube & igus Rail Cut-List CSV:
     - hardware/CARBON_TUBE_CUTLIST.csv
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
    # 1. OD30 Carbon Tube Split-Clamp Structural Lug (7075-T6 Billet, 42mm thick)
    # Grips Ø30mm roll-wrapped carbon tube externally with 0.15mm epoxy bond relief + 2x M6 Ti pinch bolts
    lug_poly = [
        (0.0, 0.0), (88.0, 0.0), (88.0, 26.0),
        (58.0, 52.0), (0.0, 52.0)
    ]
    lug_circles = [
        (26.0, 26.0, 15.1),  # Ø30.2mm bore for Ø30mm carbon tube + 0.1mm 3M DP420 epoxy film
        (72.0, 14.0, 3.1),   # M6 Titanium pinch bolt
        (72.0, 38.0, 4.1),   # Ø8mm LINAK actuator clevis pin bore
    ]
    write_dxf("hardware/cnc_7075/od30_split_clamp_lug.dxf", [lug_poly], lug_circles)
    write_svg("hardware/cnc_7075/od30_split_clamp_lug.svg", 88.0, 52.0, [lug_poly], lug_circles,
              "CNC 7075-T6 OD30 Carbon Tube Split-Clamp Lug")
    lug_tris = box_triangles(0, 0, 0, 52, 52, 42) + box_triangles(52, 0, 6, 88, 32, 36)
    write_ascii_stl("hardware/cnc_7075/od30_split_clamp_lug.stl", "od30_split_clamp_lug", lug_tris)

    # 2. igus DryLin W (WS-10-40) Width-Morphing Carriage Mount Block (480mm <-> 640mm Universal Doorway Morph)
    igus_poly = [
        (0.0, 0.0), (120.0, 0.0), (120.0, 75.0), (0.0, 75.0)
    ]
    igus_circles = [
        (20.0, 18.0, 3.1), (100.0, 18.0, 3.1),
        (20.0, 57.0, 3.1), (100.0, 57.0, 3.1),  # 4x M6 igus DryLin WJ200UM-01-10 carriage mounts
        (60.0, 37.5, 4.1),                      # Center clevis pin for 160mm width-morph actuator
    ]
    write_dxf("hardware/cnc_7075/igus_drylin_width_carriage_mount.dxf", [igus_poly], igus_circles)
    write_svg("hardware/cnc_7075/igus_drylin_width_carriage_mount.svg", 120.0, 75.0, [igus_poly], igus_circles,
              "CNC 7075-T6 igus DryLin W Width-Morphing Carriage Block")
    igus_tris = box_triangles(0, 0, 0, 120, 75, 18) + box_triangles(45, 22, 18, 75, 53, 42)
    write_ascii_stl("hardware/cnc_7075/igus_drylin_width_carriage_mount.stl", "igus_drylin_width_carriage_mount", igus_tris)

    # 3. Fidlock Auto-Latching 180-Deg Split-Saddle Hinge Block (7075-T6 Billet)
    saddle_poly = [
        (0.0, 0.0), (105.0, 0.0), (130.0, 22.0),
        (130.0, 68.0), (105.0, 90.0), (0.0, 90.0)
    ]
    saddle_circles = [
        (26.0, 45.0, 12.6),  # Ø25.2mm telescoping inner carbon column clamp bore
        (100.0, 45.0, 5.0),  # Ø10mm shoulder-bolt thrust-bearing saddle pivot
        (68.0, 45.0, 4.0),   # Fidlock magnetic-mechanical plunger lock (90-deg seated/perch)
        (100.0, 77.0, 4.0),  # Fidlock magnetic-mechanical plunger lock (0-deg open walking)
    ]
    write_dxf("hardware/cnc_7075/fidlock_split_saddle_hinge.dxf", [saddle_poly], saddle_circles)
    write_svg("hardware/cnc_7075/fidlock_split_saddle_hinge.svg", 130.0, 90.0, [saddle_poly], saddle_circles,
              "CNC 7075-T6 Fidlock Split-Saddle Hinge")
    saddle_tris = box_triangles(0, 0, 0, 55, 90, 32) + box_triangles(55, 15, 6, 130, 75, 26)
    write_ascii_stl("hardware/cnc_7075/fidlock_split_saddle_hinge.stl", "fidlock_split_saddle_hinge", saddle_tris)

    # 4. Rear Pancake FOC Hub Motor Dropout + VL53L1X Cliff-Sensor Pocket (7075-T6 Billet)
    dropout_poly = [
        (0.0, 0.0), (115.0, 0.0), (115.0, 65.0),
        (75.0, 95.0), (0.0, 95.0)
    ]
    dropout_circles = [
        (25.0, 70.0, 15.1),  # Ø30mm lower carbon side-rail bore
        (80.0, 32.0, 6.0),   # Ø12mm anti-rotation FOC hub motor axle slot
        (25.0, 22.0, 3.1),   # M6 VL53L1X rear step-drop ToF sensor mount
    ]
    write_dxf("hardware/cnc_7075/foc_hub_motor_dropout.dxf", [dropout_poly], dropout_circles)
    write_svg("hardware/cnc_7075/foc_hub_motor_dropout.svg", 115.0, 95.0, [dropout_poly], dropout_circles,
              "CNC 7075-T6 Rear FOC Hub Motor Dropout + Cliff Sensor Mount")
    dropout_tris = box_triangles(0, 0, 0, 115, 95, 16)
    write_ascii_stl("hardware/cnc_7075/foc_hub_motor_dropout.stl", "foc_hub_motor_dropout", dropout_tris)


def generate_3d_print_stls():
    # 1. Forearm Load-Cell Cockpit & Switch Pod (Holds 20kg Strain-Gauge Load Cell + Forearm Gel Trough)
    tris = []
    tris.extend(box_triangles(0, 0, 0, 190, 95, 8))       # Load-cell flexure base plate
    tris.extend(box_triangles(0, 0, 8, 190, 10, 36))      # Left ergonomic forearm lip
    tris.extend(box_triangles(0, 85, 8, 190, 95, 36))     # Right ergonomic forearm lip
    tris.extend(box_triangles(190, 15, 0, 240, 80, 32))   # Sealed switch & OLED status pod
    write_ascii_stl("hardware/3d_print/forearm_loadcell_cockpit.stl", "forearm_loadcell_cockpit", tris)

    # 2. Boa-Dial Orthopedic "Air-Float" Ankle Cradle Shell (Contoured tibial/shin trough with heel cutout)
    cradle_tris = []
    cradle_tris.extend(box_triangles(0, 0, 0, 220, 115, 8))     # Contoured tibial base
    cradle_tris.extend(box_triangles(0, 0, 8, 220, 12, 48))     # Lateral calf stabilizer wall
    cradle_tris.extend(box_triangles(0, 103, 8, 220, 115, 48))  # Medial calf stabilizer wall
    cradle_tris.extend(box_triangles(0, 30, -28, 48, 85, 0))    # Quick-release dovetail lug for Ø30mm column
    write_ascii_stl("hardware/3d_print/boa_ankle_cradle_shell.stl", "boa_ankle_cradle_shell", cradle_tris)


def generate_universal_cutlist_csv():
    rows = [
        ["Part ID", "Component / Tube Name", "Material & Spec", "Outer Dia / Profile (mm)", "Wall (mm)", "Exact Cut Length (mm)", "Qty", "Target Subsystem & Notes"],
        ["CF-01", "Lower Side Chassis Rails (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø30.0", "2.5", "640.0", 2, "Connects front Tente casters to rear FOC hub dropouts (fits 680mm elevator/bathroom depth)"],
        ["CF-02", "Vertical Outer Telescoping Columns (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø30.0", "2.5", "540.0", 2, "Fixed vertical pillars; houses igus DryLin polymer bushings inside top collar"],
        ["CF-03", "Vertical Inner Lifting Columns (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø25.0", "2.5", "520.0", 2, "Telescopes 300mm inside CF-02 (Saddle: 420mm->720mm; Tray: 580mm->880mm)"],
        ["CF-04", "Upper Forearm Cockpit Support Tubes (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø25.0", "2.0", "420.0", 2, "Supports 24-bit Load-Cell Forearm Troughs & Slide-Bridge Kitchen Tray"],
        ["CF-05", "Split-Saddle Cantilever Arms (L & R)", "3K Roll-Wrapped Autoclave Carbon Tube", "Ø25.0", "3.0", "230.0", 2, "Pivots 90-deg on Fidlock 7075-T6 Hinge Block behind user's pelvis"],
        ["IG-01", "Front Lower Width-Morphing Linear Rail", "igus DryLin W Hard-Anodized Al Rail (WS-10-40)", "40.0 x 10.0", "Solid", "580.0", 1, "Allows continuous 480mm (18.9in) to 640mm (25.2in) doorway width morphing"],
        ["IG-02", "Front Upper Synchronizer Linear Rail", "igus DryLin W Hard-Anodized Al Rail (WS-10-40)", "40.0 x 10.0", "Solid", "580.0", 1, "Keeps vertical columns parallel during width morphing while leaving rear 100% open"],
        ["LK-01", "Primary Sit-to-Stand Lifting Columns", "LINAK LA23 / TiMOTION TA16 Medical Actuator", "Compact Medical", "IPX6", "300.0 Stroke (455mm Retracted)", 2, "Synchronized Hall-effect closed loop; 1500N each (3000N / 300kgf combined)"],
        ["LK-02", "Horizontal Width-Morphing Actuator", "LINAK / TiMOTION Micro Linear Actuator", "Compact IP66", "IP66", "160.0 Stroke (245mm Retracted)", 1, "Drives 480mm (Bathroom) <-> 550mm (Indoor) <-> 640mm (Hospital/Perch) presets"],
    ]
    with open("hardware/CARBON_TUBE_CUTLIST.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == "__main__":
    ensure_dirs()
    generate_cnc_7075_parts()
    generate_3d_print_stls()
    generate_universal_cutlist_csv()
    print("Generated CNC 7075-T6 CAD files, 3D print STLs, and Universal Cutlist CSV successfully!")
