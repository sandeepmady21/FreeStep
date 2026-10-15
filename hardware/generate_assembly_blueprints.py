#!/usr/bin/env python3
"""
Generates the 6 Engineering Assembly Blueprint SVG Sheets (hardware/blueprints/blueprint_01..06.svg),
the Printable Markdown Blueprint Manual (hardware/ASSEMBLY_BLUEPRINTS.md),
and the Interactive HTML5 Exploded CAD Blueprint Viewer (docs/assembly_blueprints.html).
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(BASE_DIR)
BP_DIR = os.path.join(BASE_DIR, "blueprints")
DOCS_DIR = os.path.join(REPO_DIR, "docs")
os.makedirs(BP_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)


def svg_header(title, sheet_num, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="820" viewBox="0 0 1200 820">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" stroke-width="0.7"/>
    </pattern>
    <pattern id="grid100" width="100" height="100" patternUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="url(#grid)"/>
      <path d="M 100 0 L 0 0 0 100" fill="none" stroke="#334155" stroke-width="1.2"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e"/>
    </marker>
  </defs>
  <rect width="1200" height="820" fill="#0b1120"/>
  <rect x="20" y="20" width="1160" height="780" fill="url(#grid100)" stroke="#38bdf8" stroke-width="2"/>
  <!-- Title Block Header -->
  <rect x="20" y="20" width="1160" height="58" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="40" y="46" fill="#38bdf8" font-family="monospace" font-size="18" font-weight="bold">{title}</text>
  <text x="40" y="66" fill="#94a3b8" font-family="monospace" font-size="12">{subtitle}</text>
  <text x="1160" y="46" fill="#22c55e" font-family="monospace" font-size="16" font-weight="bold" text-anchor="end">SHEET {sheet_num} OF 6</text>
  <text x="1160" y="66" fill="#64748b" font-family="monospace" font-size="11" text-anchor="end">ELDERSTEP PRO (9.85 kg STANDARD-COTS EDITION) | UNITS: MM</text>
'''


def svg_footer(notes_left, notes_right):
    return f'''  <!-- Engineering Title Block Footer -->
  <rect x="20" y="745" width="1160" height="55" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>
  <line x1="620" y1="745" x2="620" y2="800" stroke="#38bdf8" stroke-width="1"/>
  <text x="35" y="768" fill="#e2e8f0" font-family="monospace" font-size="12" font-weight="bold">{notes_left[0]}</text>
  <text x="35" y="788" fill="#94a3b8" font-family="monospace" font-size="11">{notes_left[1]}</text>
  <text x="635" y="768" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold">{notes_right[0]}</text>
  <text x="635" y="788" fill="#94a3b8" font-family="monospace" font-size="11">{notes_right[1]}</text>
</svg>
'''


def make_sheet_01():
    svg = svg_header(
        "BLUEPRINT 01: MASTER CHASSIS ORTHOGRAPHIC & KINEMATIC ENVELOPE",
        "1",
        "Side Elevation (12-Deg Nose-Over-Toes Rake) + Front Doorway Clearance View (495mm Universal Envelope)"
    )
    svg += '''
  <!-- SIDE VIEW (LEFT PANEL) -->
  <text x="60" y="110" fill="#38bdf8" font-family="monospace" font-size="15" font-weight="bold">[A] SIDE ELEVATION (SEATED 420MM vs STANDING 713MM)</text>
  <!-- Floor Line -->
  <line x1="50" y1="660" x2="640" y2="660" stroke="#94a3b8" stroke-width="2" stroke-dasharray="8,4"/>
  <text x="55" y="680" fill="#94a3b8" font-family="monospace" font-size="11">FINISHED FLOOR LEVEL (0.0 MM)</text>

  <!-- Rear 6.5" (165mm) Hub Wheel -->
  <circle cx="150" cy="594" r="66" fill="#1e293b" stroke="#f43f5e" stroke-width="3"/>
  <circle cx="150" cy="594" r="42" fill="#0f172a" stroke="#f43f5e" stroke-width="1.5"/>
  <circle cx="150" cy="594" r="8" fill="#38bdf8"/>
  <text x="150" y="700" fill="#f43f5e" font-family="monospace" font-size="11" text-anchor="middle">REAR 6.5" (165mm) IP65 HUB WHEEL</text>

  <!-- Front 74mm Low-Profile Twin 64mm Skate Caster -->
  <circle cx="515" cy="634" r="26" fill="#1e293b" stroke="#22c55e" stroke-width="2.5"/>
  <circle cx="515" cy="634" r="6" fill="#38bdf8"/>
  <text x="515" y="700" fill="#22c55e" font-family="monospace" font-size="11" text-anchor="middle">FRONT 64mm SKATE CASTER (74mm NOSE)</text>

  <!-- Lower Carbon U-Base Leg (ø30mm) -->
  <rect x="150" y="600" width="370" height="16" rx="6" fill="#334155" stroke="#e2e8f0" stroke-width="2"/>
  <!-- LiFePO4 Battery Ballast at Front Nose -->
  <rect x="415" y="576" width="85" height="24" rx="4" fill="#166534" stroke="#22c55e" stroke-width="1.5"/>
  <text x="457" y="592" fill="#dcfce7" font-family="monospace" font-size="9" text-anchor="middle">24V LiFePO4 (1kg)</text>

  <!-- 12-Deg Base Lug -->
  <polygon points="310,616 385,616 375,555 320,555" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2"/>
  <text x="348" y="634" fill="#38bdf8" font-family="monospace" font-size="10" text-anchor="middle">12° CNC LUG</text>

  <!-- Outer Carbon Barrel (ø35mm, inclined 12 deg forward) -->
  <line x1="348" y1="595" x2="396" y2="370" stroke="#475569" stroke-width="22" stroke-linecap="round"/>
  <line x1="348" y1="595" x2="396" y2="370" stroke="#94a3b8" stroke-width="18" stroke-linecap="round"/>

  <!-- Inner Carbon Plunger Extended (+300mm along 12-deg = +293mm UP, +62mm FWD) -->
  <line x1="385" y1="420" x2="442" y2="155" stroke="#0284c7" stroke-width="14" stroke-linecap="round"/>

  <!-- Split Saddle at Seated (420mm) and Standing (713mm) -->
  <rect x="275" y="370" width="95" height="18" rx="8" fill="#f59e0b" stroke="#fef08a" stroke-width="2"/>
  <text x="265" y="383" fill="#fef08a" font-family="monospace" font-size="11" text-anchor="end">SADDLE LOW: 420mm (Toilet/Bed)</text>

  <rect x="320" y="195" width="95" height="18" rx="8" fill="#f59e0b" stroke="#fef08a" stroke-width="2" stroke-dasharray="4,2"/>
  <text x="310" y="208" fill="#fef08a" font-family="monospace" font-size="11" text-anchor="end">SADDLE HIGH: 713mm (+293mm UP, +62mm FWD)</text>

  <!-- Upper Handlebar Halo + MGN9C Slide-Bridge Kitchen Tray -->
  <rect x="380" y="140" width="160" height="14" rx="5" fill="#334155" stroke="#38bdf8" stroke-width="2"/>
  <rect x="460" y="126" width="165" height="10" rx="3" fill="#06b6d4" stroke="#cffafe" stroke-width="1.5"/>
  <text x="542" y="118" fill="#22d3ee" font-family="monospace" font-size="11" text-anchor="middle">MGN9C KITCHEN TRAY (+300mm REACH)</text>

  <!-- Wheelbase Dimension (580mm) -->
  <line x1="150" y1="720" x2="515" y2="720" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  <text x="332" y="735" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">WHEELBASE: 580.0 MM</text>

  <!-- FRONT VIEW (RIGHT PANEL) -->
  <text x="700" y="110" fill="#38bdf8" font-family="monospace" font-size="15" font-weight="bold">[B] FRONT ELEVATION (495MM BATHROOM FIT)</text>
  <line x1="680" y1="660" x2="1150" y2="660" stroke="#94a3b8" stroke-width="2" stroke-dasharray="8,4"/>

  <!-- 510mm Indian Bathroom Door Frame Reference -->
  <rect x="705" y="120" width="420" height="540" fill="none" stroke="#f43f5e" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="915" y="138" fill="#f43f5e" font-family="monospace" font-size="11" text-anchor="middle">MIN INDIAN BATHROOM DOOR: 510mm (20.0")</text>

  <!-- Left & Right Carbon Columns (430mm Inside Clearance, 495mm Max Outer Width) -->
  <rect x="720" y="210" width="24" height="400" rx="6" fill="#334155" stroke="#38bdf8" stroke-width="2"/>
  <rect x="1086" y="210" width="24" height="400" rx="6" fill="#334155" stroke="#38bdf8" stroke-width="2"/>

  <!-- Upper Cross Halo & Kitchen Tray -->
  <rect x="720" y="190" width="390" height="20" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>
  <rect x="750" y="176" width="330" height="12" rx="4" fill="#06b6d4" stroke="#cffafe" stroke-width="1.5"/>

  <!-- Split Saddle Halves (Latched Center vs Folded Out) -->
  <rect x="744" y="370" width="168" height="22" rx="6" fill="#f59e0b" stroke="#fef08a" stroke-width="2"/>
  <rect x="918" y="370" width="168" height="22" rx="6" fill="#f59e0b" stroke="#fef08a" stroke-width="2"/>
  <circle cx="915" cy="381" r="7" fill="#22c55e" stroke="#ffffff" stroke-width="1.5"/>
  <text x="915" y="358" fill="#22c55e" font-family="monospace" font-size="11" text-anchor="middle">N52 + 10mm SS CONICAL LATCH (12 kN)</text>

  <!-- Lower Front Cross Bridge + LD19 360 LiDAR Shroud -->
  <rect x="735" y="592" width="360" height="18" rx="6" fill="#334155" stroke="#94a3b8" stroke-width="2"/>
  <circle cx="915" cy="585" r="18" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
  <text x="915" y="558" fill="#38bdf8" font-family="monospace" font-size="10" text-anchor="middle">LD19 360° LiDAR + VL53L1X CLIFF</text>

  <!-- Left & Right Wheels -->
  <rect x="716" y="580" width="28" height="80" rx="8" fill="#1e293b" stroke="#f43f5e" stroke-width="2"/>
  <rect x="1086" y="580" width="28" height="80" rx="8" fill="#1e293b" stroke="#f43f5e" stroke-width="2"/>

  <!-- Dimension Arrows (430mm Inside, 495mm Total Outer) -->
  <line x1="744" y1="470" x2="1086" y2="470" stroke="#22c55e" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  <text x="915" y="462" fill="#22c55e" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">HIP / TOILET CLEARANCE: 430.0 MM</text>

  <line x1="716" y1="720" x2="1114" y2="720" stroke="#38bdf8" stroke-width="1.5" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  <text x="915" y="735" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">TOTAL OUTER WIDTH: 495.0 MM (19.5")</text>
'''
    svg += svg_footer(
        ("CRITICAL GEOMETRY: 12.0° Forward Column Rake ('Nose-Over-Toes' Biomechanics)",
         "300mm Actuator Stroke = +293mm Vertical Lift & +62mm Forward Weight Shift"),
        ("TOLERANCES & BONDING: 3M Scotch-Weld DP420 + 110um Glass Microspheres",
         "Ensure Left & Right Columns are clamped parallel within +-0.2mm during 24h cure")
    )
    with open(os.path.join(BP_DIR, "blueprint_01_master_frame_orthographic.svg"), "w") as f:
        f.write(svg)


def make_sheet_02():
    svg = svg_header(
        "BLUEPRINT 02: TELESCOPING CARBON COLUMN & STANDARD ACTUATOR CARTRIDGE",
        "2",
        "Cross-Section of ø35x31mm Outer Carbon Barrel + ø30x26mm Inner Plunger + Standard 24V 300mm IP65 Inline Actuator"
    )
    svg += '''
  <!-- CROSS-SECTION DIAGRAM (HORIZONTAL EXPLODED / SECTIONED VIEW) -->
  <text x="50" y="115" fill="#38bdf8" font-family="monospace" font-size="15" font-weight="bold">[A] FULL SECTION VIEW: HOW THE STANDARD 24V ACTUATOR DROPS INSIDE THE CARBON TUBES</text>

  <!-- 12-Deg Base Lug (Left Side / Bottom of Column) -->
  <rect x="70" y="230" width="90" height="220" rx="10" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2.5"/>
  <text x="115" y="215" fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[1] 12° CNC BASE LUG</text>

  <!-- Outer Carbon Tube (ø35mm OD x ø31mm ID x 460mm) -->
  <rect x="130" y="250" width="460" height="22" fill="#334155" stroke="#e2e8f0" stroke-width="1.5"/>
  <rect x="130" y="408" width="460" height="22" fill="#334155" stroke="#e2e8f0" stroke-width="1.5"/>
  <text x="360" y="240" fill="#e2e8f0" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">[2] OUTER CARBON BARREL: ø35mm OD x ø31mm ID x 460mm (CF-01)</text>

  <!-- Lathe-Turned POM (Delrin) Sleeve Bushings (x2 per column) -->
  <rect x="530" y="272" width="60" height="16" fill="#22c55e" stroke="#ffffff" stroke-width="1.5"/>
  <rect x="530" y="392" width="60" height="16" fill="#22c55e" stroke="#ffffff" stroke-width="1.5"/>
  <rect x="290" y="272" width="60" height="16" fill="#22c55e" stroke="#ffffff" stroke-width="1.5"/>
  <rect x="290" y="392" width="60" height="16" fill="#22c55e" stroke="#ffffff" stroke-width="1.5"/>
  <!-- Silicone Wiper O-Ring -->
  <circle cx="594" cy="280" r="6" fill="#f43f5e"/>
  <circle cx="594" cy="400" r="6" fill="#f43f5e"/>
  <text x="565" y="215" fill="#22c55e" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[3] LATHE-TURNED DELRIN SLEEVES + O-RING</text>

  <!-- Inner Carbon Plunger Tube (ø30mm OD x ø26mm ID x 440mm) -->
  <rect x="290" y="288" width="520" height="16" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/>
  <rect x="290" y="376" width="520" height="16" fill="#0284c7" stroke="#bae6fd" stroke-width="1.5"/>
  <text x="680" y="275" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">[4] INNER CARBON PLUNGER: ø30mm OD x ø26mm ID x 440mm (CF-02)</text>

  <!-- Standard 24V 300mm Inline Linear Actuator Cartridge Inside -->
  <rect x="145" y="310" width="380" height="60" rx="6" fill="#475569" stroke="#f59e0b" stroke-width="2.5"/>
  <text x="335" y="336" fill="#fef08a" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">[5] STANDARD 24V 300mm INLINE ACTUATOR CARTRIDGE</text>
  <text x="335" y="354" fill="#e2e8f0" font-family="monospace" font-size="10" text-anchor="middle">(1500N Self-Locking, IP65 Waterproof, Built-In Hall Encoder)</text>

  <!-- Extending Stainless Actuator Rod -->
  <rect x="525" y="326" width="295" height="28" fill="#94a3b8" stroke="#ffffff" stroke-width="1.5"/>
  <text x="670" y="344" fill="#0f172a" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">STAINLESS INNER ROD (300mm STROKE)</text>

  <!-- Top CNC Clevis Cap (inhouse_sfu1204_ballscrew_column_cap.dxf) -->
  <rect x="810" y="280" width="75" height="120" rx="8" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2.5"/>
  <text x="847" y="255" fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[6] TOP CNC CAP</text>

  <!-- Bottom & Top M8 Quick-Release Clevis Pins -->
  <circle cx="115" cy="340" r="12" fill="#f43f5e" stroke="#ffffff" stroke-width="2"/>
  <text x="115" y="344" fill="#ffffff" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle">M8</text>
  <circle cx="835" cy="340" r="12" fill="#f43f5e" stroke="#ffffff" stroke-width="2"/>
  <text x="835" y="344" fill="#ffffff" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle">M8</text>

  <text x="115" y="480" fill="#f43f5e" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[7] LOWER M8 CLEVIS PIN</text>
  <text x="835" y="430" fill="#f43f5e" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[8] UPPER M8 CLEVIS PIN</text>

  <!-- CALLOUT TABLE AT BOTTOM -->
  <rect x="50" y="515" width="1100" height="205" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="70" y="542" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">SUB-ASSEMBLY 02 BILL OF MATERIALS & STEP-BY-STEP ASSEMBLY PROCEDURE (PER LEG, BUILD 2X):</text>
  <text x="70" y="568" fill="#e2e8f0" font-family="monospace" font-size="12">[1] 12° Base Lug (12deg_incline_base_lug.dxf): Bond ø35mm outer carbon barrel [2] into 35.2mm socket using 3M DP420 epoxy.</text>
  <text x="70" y="592" fill="#22c55e" font-family="monospace" font-size="12">[3] Lathe-Turned POM (Delrin) Bushings (delrin_telescoping_column_bushing.stl): 31.0mm OD x 30.05mm ID x 40mm. Press-fit 2 per leg.</text>
  <text x="70" y="616" fill="#38bdf8" font-family="monospace" font-size="12">[4] Inner Carbon Plunger (ø30x26mm x 440mm): Glides inside Delrin bushings [3]—carries 100% of Grandma's side/bending loads!</text>
  <text x="70" y="640" fill="#fef08a" font-family="monospace" font-size="12">[5] Standard 24V 300mm Inline Actuator (ACT-01): Slide inside carbon tubes; secure bottom & top eyes with M8x45mm clevis pins [7][8].</text>
  <text x="70" y="664" fill="#f43f5e" font-family="monospace" font-size="12">[7][8] 3-Minute Maintenance Swap: Pull upper & lower M8 clevis pins to remove/replace the standard actuator cartridge anytime!</text>
  <text x="70" y="692" fill="#94a3b8" font-family="monospace" font-size="12">LIFT SPEED & FORCE: 32 mm/s (9.3s full stroke) | 1500 N (150 kgf) per leg = 300 kgf total lift | Self-locking worm gear (zero back-drive)</text>
'''
    svg += svg_footer(
        ("STRUCTURAL PRINCIPLE: Bending Decoupling via Carbon/Delrin Telescoping Sleeves",
         "The internal 24V actuator experiences pure axial compression; carbon tubes take 100% bending moment."),
        ("WATERPROOFING: IP65 Sealed Actuator Cartridge + Top 30mmx2.5mm Silicone Wiper O-Ring",
         "100% immune to wet Indian bathroom floors and humidity.")
    )
    with open(os.path.join(BP_DIR, "blueprint_02_telescoping_carbon_actuator_column.svg"), "w") as f:
        f.write(svg)


def make_sheet_03():
    svg = svg_header(
        "BLUEPRINT 03: REAR 6.5\" (165MM) SEALED BLDC HUB WHEEL & DROPOUT ASSEMBLY",
        "3",
        "Standard IP65 Hoverboard/AMR Hall-Sensor Hub Motor + CNC 7075-T6 ø16mm D-Axle Clamp Dropout (rear_16mm_hub_axle_dropout.dxf)"
    )
    svg += '''
  <text x="50" y="115" fill="#38bdf8" font-family="monospace" font-size="15" font-weight="bold">[A] EXPLODED VIEW: REAR SEALED HUB MOTOR TO CARBON LEG DROPOUT (5-MINUTE BOLT-ON)</text>

  <!-- ø30mm Rear Carbon Base Leg -->
  <rect x="80" y="180" width="260" height="44" rx="8" fill="#334155" stroke="#e2e8f0" stroke-width="2"/>
  <text x="210" y="207" fill="#ffffff" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">[1] ø30mm CARBON REAR LEG (CF-03)</text>

  <!-- CNC 7075-T6 Rear Hub Dropout Plate -->
  <rect x="360" y="160" width="160" height="270" rx="14" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="440" cy="202" r="26" fill="#0f172a" stroke="#22c55e" stroke-width="2"/>
  <text x="440" y="206" fill="#22c55e" font-family="monospace" font-size="10" text-anchor="middle">ø30.2 BORE</text>

  <!-- ø16mm D-Shaped Axle Clamp Slot -->
  <circle cx="440" cy="360" r="18" fill="#0f172a" stroke="#f43f5e" stroke-width="2.5"/>
  <line x1="360" y1="360" x2="520" y2="360" stroke="#0f172a" stroke-width="6"/>
  <text x="440" y="325" fill="#f43f5e" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[2] ø16.0mm D-SHAFT CLAMP</text>

  <!-- 4x M6x35 Clamp Bolts -->
  <circle cx="395" cy="335" r="6" fill="#fef08a"/>
  <circle cx="485" cy="335" r="6" fill="#fef08a"/>
  <circle cx="395" cy="385" r="6" fill="#fef08a"/>
  <circle cx="485" cy="385" r="6" fill="#fef08a"/>
  <text x="440" y="455" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">[2] CNC DROPOUT (rear_16mm_hub_axle_dropout.dxf)</text>

  <!-- Exploded Dashed Alignment Line -->
  <line x1="440" y1="360" x2="780" y2="360" stroke="#f43f5e" stroke-width="2" stroke-dasharray="8,6" marker-end="url(#arrowRed)"/>

  <!-- Standard 6.5" (165mm) Sealed BLDC Hub Motor Wheel -->
  <circle cx="850" cy="360" r="155" fill="#1e293b" stroke="#f43f5e" stroke-width="4"/>
  <circle cx="850" cy="360" r="110" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
  <circle cx="850" cy="360" r="22" fill="#475569" stroke="#fef08a" stroke-width="3"/>
  <text x="850" y="300" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold" text-anchor="middle">[3] STANDARD 6.5" (165mm) BLDC HUB</text>
  <text x="850" y="322" fill="#e2e8f0" font-family="monospace" font-size="11" text-anchor="middle">IP65 Waterproof Sealed Shell</text>
  <text x="850" y="415" fill="#22c55e" font-family="monospace" font-size="11" text-anchor="middle">3-Phase + 5-Pin Hall Sensor Cable</text>
  <text x="850" y="435" fill="#fef08a" font-family="monospace" font-size="11" text-anchor="middle">100% Saree & Loose-Clothing Safe!</text>

  <!-- CALLOUT TABLE -->
  <rect x="50" y="545" width="1100" height="175" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="70" y="572" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">SUB-ASSEMBLY 03 TORQUE SPECS & WIRING (BUILD 2X - LEFT & RIGHT):</text>
  <text x="70" y="598" fill="#e2e8f0" font-family="monospace" font-size="12">1. Bond & pinch-bolt rear carbon tube [1] into upper ø30.2mm socket of CNC Dropout [2] (2x M5x25mm Socket Head Cap Screws, 6 Nm).</text>
  <text x="70" y="622" fill="#fef08a" font-family="monospace" font-size="12">2. Insert the standard ø16mm D-flat stator shaft of the 6.5" BLDC Hub Wheel [3] into the lower split clamp of [2].</text>
  <text x="70" y="646" fill="#22c55e" font-family="monospace" font-size="12">3. Torque the 4x M6x35mm Grade 10.9 clamp bolts + Blue Loctite 243 to 12.0 Nm. Route Hall & Phase wires up inside the rear carbon leg.</text>
  <text x="70" y="670" fill="#38bdf8" font-family="monospace" font-size="12">4. Connect Phase (U/V/W) + 5-Pin Hall plug to Dual Sinusoidal FOC Controller (DRV-02) for zero-cogging push & 40 Nm active brake hold.</text>
'''
    svg += svg_footer(
        ("WHY THIS WINS: Global 50M/yr Standard ø16mm D-Shaft Hoverboard/AMR Wheel",
         "Available from 20+ Indian suppliers on Robu.in / Amazon / IndiaMART with zero vendor lock-in."),
        ("SAFETY RATING: IP65 Sealed Enclosure + Zero Exposed Belts or Outrunner Shells",
         "Safe around sarees, nightgowns, wet bathroom floors, and hospital washdowns.")
    )
    with open(os.path.join(BP_DIR, "blueprint_03_rear_65in_hub_wheel_dropout.svg"), "w") as f:
        f.write(svg)


def make_sheet_04():
    svg = svg_header(
        "BLUEPRINT 04: ULTRA-LOW 74MM FRONT TWIN-SKATE CASTER ASSEMBLY",
        "4",
        "CNC 7075-T6 Swivel Fork (inhouse_twin_64mm_caster_fork.dxf) + SKF 51104 Thrust Bearing + Twin 64mm 82A PU Skate Wheels"
    )
    svg += '''
  <text x="50" y="115" fill="#38bdf8" font-family="monospace" font-size="15" font-weight="bold">[A] VERTICAL STACK & FRONT SECTION: ACHIEVING THE 74.0 MM (2.9") UNDER-BED NOSE HEIGHT</text>

  <!-- Front Nose of Carbon Tube -->
  <rect x="140" y="180" width="280" height="48" rx="8" fill="#334155" stroke="#e2e8f0" stroke-width="2"/>
  <text x="280" y="208" fill="#ffffff" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">[1] FRONT NOSE OF ø30mm CARBON LEG</text>

  <!-- SKF 51104 Axial Thrust Ball Bearing (20mm ID x 35mm OD x 10mm) -->
  <rect x="215" y="245" width="130" height="26" rx="4" fill="#f59e0b" stroke="#fef08a" stroke-width="2"/>
  <text x="460" y="263" fill="#fef08a" font-family="monospace" font-size="12" font-weight="bold">[2] SKF 51104 AXIAL THRUST BEARING (20x35x10mm)</text>

  <!-- CNC 7075-T6 Swivel Fork (inhouse_twin_64mm_caster_fork.dxf) -->
  <polygon points="170,285 390,285 410,480 375,480 375,325 185,325 185,480 150,480" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2.5"/>
  <text x="460" y="315" fill="#38bdf8" font-family="monospace" font-size="12" font-weight="bold">[3] CNC 7075-T6 SWIVEL FORK (inhouse_twin_64mm_caster_fork.dxf)</text>

  <!-- M10x45 Stainless Kingpin Bolt -->
  <rect x="268" y="165" width="24" height="175" rx="3" fill="#f43f5e" stroke="#ffffff" stroke-width="1.5"/>
  <text x="280" y="155" fill="#f43f5e" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[4] M10 KINGPIN + NYLOC NUT</text>

  <!-- Twin 64mm 82A Decathlon Inline Skate PU Wheels + ABEC-9 608RS Bearings -->
  <rect x="195" y="345" width="72" height="190" rx="18" fill="#22c55e" stroke="#dcfce7" stroke-width="2.5"/>
  <rect x="293" y="345" width="72" height="190" rx="18" fill="#22c55e" stroke="#dcfce7" stroke-width="2.5"/>
  <!-- 8mm Center Spacer -->
  <rect x="267" y="425" width="26" height="30" fill="#94a3b8" stroke="#ffffff" stroke-width="1.5"/>

  <!-- M8x75mm Stainless Axle Bolt -->
  <line x1="130" y1="440" x2="430" y2="440" stroke="#fef08a" stroke-width="8"/>
  <text x="460" y="445" fill="#fef08a" font-family="monospace" font-size="12" font-weight="bold">[5] M8x75mm AXLE + TWIN 64mm 82A SKATE WHEELS (ABEC-9 608RS)</text>

  <!-- Floor Line & Total 74mm Height Dimension -->
  <line x1="80" y1="535" x2="550" y2="535" stroke="#94a3b8" stroke-width="2" stroke-dasharray="8,4"/>
  <line x1="105" y1="180" x2="105" y2="535" stroke="#22c55e" stroke-width="2" marker-start="url(#arrow)" marker-end="url(#arrow)"/>
  <text x="95" y="360" fill="#22c55e" font-family="monospace" font-size="13" font-weight="bold" text-anchor="end">TOTAL: 74.0 MM (2.9")</text>

  <!-- CALLOUT TABLE -->
  <rect x="50" y="565" width="1100" height="155" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="70" y="592" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">SUB-ASSEMBLY 04 STEP-BY-STEP ASSEMBLY (BUILD 2X - FRONT LEFT & RIGHT):</text>
  <text x="70" y="618" fill="#e2e8f0" font-family="monospace" font-size="12">1. Seat the SKF 51104 axial thrust bearing [2] into the top 35mm pocket of the CNC Caster Fork [3] and bolt to front nose [1] with M10 kingpin [4].</text>
  <text x="70" y="642" fill="#22c55e" font-family="monospace" font-size="12">2. Slide M8x75mm stainless bolt [5] through Left Fork Leg -> 64mm 82A Skate Wheel -> 8mm Spacer -> Second 64mm Skate Wheel -> Right Fork Leg.</text>
  <text x="70" y="666" fill="#fef08a" font-family="monospace" font-size="12">3. Why Twin 64mm 82A Wheels? Half the floor scrubbing torque when swiveling on bathroom tiles, silent over grout lines, and 74mm low clearance.</text>
'''
    svg += svg_footer(
        ("STANDARD COTS PARTS: Decathlon Oxelo 64mm 82A PU Wheels + Standard 608RS & 51104 Bearings",
         "Available off the shelf across India for ₹1,400 total."),
        ("THRESHOLD CLIMBING: 64mm Wheel Diameter + 18mm Trail Angle",
         "Climbs 15-40mm Indian bathroom marble door thresholds smoothly without caster flutter.")
    )
    with open(os.path.join(BP_DIR, "blueprint_04_front_74mm_twin_skate_caster.svg"), "w") as f:
        f.write(svg)


def make_sheet_05():
    svg = svg_header(
        "BLUEPRINT 05: 180° SPLIT-SADDLE PIVOT HINGE & N52 CONICAL SHEAR LATCH",
        "5",
        "Top-Down Kinematic View: Open Entry Mode (180° Flush) vs. Latched Perch/Transfer Mode (12 kN Stainless Conical Shear Lock)"
    )
    svg += '''
  <text x="50" y="115" fill="#38bdf8" font-family="monospace" font-size="15" font-weight="bold">[A] TOP-DOWN VIEW: 180° SPLIT-SADDLE HINGE + SELF-CENTERING N52 CONICAL SHEAR LATCH</text>

  <!-- Left & Right ø30mm Inner Carbon Columns -->
  <circle cx="220" cy="310" r="34" fill="#0284c7" stroke="#ffffff" stroke-width="2.5"/>
  <text x="220" y="314" fill="#ffffff" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">LEFT ø30</text>

  <circle cx="980" cy="310" r="34" fill="#0284c7" stroke="#ffffff" stroke-width="2.5"/>
  <text x="980" y="314" fill="#ffffff" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">RIGHT ø30</text>

  <!-- CNC 7075-T6 Pivot Hinge Clamps (saddle_180_pivot_hinge.dxf) -->
  <rect x="240" y="275" width="85" height="70" rx="10" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="300" cy="310" r="16" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
  <text x="282" y="260" fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[1] 608RS PIVOT HINGE</text>

  <rect x="875" y="275" width="85" height="70" rx="10" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2"/>
  <circle cx="900" cy="310" r="16" fill="#f59e0b" stroke="#ffffff" stroke-width="2"/>
  <text x="918" y="260" fill="#38bdf8" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">[1] 608RS PIVOT HINGE</text>

  <!-- Left & Right Cushioned Split-Saddle Halves (CLOSED / LATCHED POSITION) -->
  <rect x="310" y="265" width="275" height="90" rx="22" fill="#f59e0b" stroke="#fef08a" stroke-width="2.5"/>
  <text x="445" y="315" fill="#0f172a" font-family="monospace" font-size="13" font-weight="bold" text-anchor="middle">[2] LEFT SADDLE PAD (CLOSED)</text>

  <rect x="615" y="265" width="275" height="90" rx="22" fill="#f59e0b" stroke="#fef08a" stroke-width="2.5"/>
  <text x="755" y="315" fill="#0f172a" font-family="monospace" font-size="13" font-weight="bold" text-anchor="middle">[2] RIGHT SADDLE PAD (CLOSED)</text>

  <!-- Center N52 + 45-Deg Conical 304 Stainless Shear Latch (inhouse_n52_conical_saddle_latch.dxf) -->
  <rect x="565" y="260" width="70" height="100" rx="8" fill="#166534" stroke="#22c55e" stroke-width="3"/>
  <circle cx="600" cy="285" r="9" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.5"/>
  <circle cx="600" cy="310" r="12" fill="#f43f5e" stroke="#ffffff" stroke-width="1.5"/>
  <circle cx="600" cy="335" r="9" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.5"/>
  <text x="600" y="238" fill="#22c55e" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">[3] N52 MAGNET + TWIN 10mm</text>
  <text x="600" y="252" fill="#22c55e" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">CONICAL 304SS SHEAR PINS (12 kN)</text>

  <!-- Dashed Ghost View of Saddle Halves Swung 180° Outward for Open Walk-In Entry -->
  <rect x="150" y="365" width="80" height="160" rx="18" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="190" y="450" fill="#38bdf8" font-family="monospace" font-size="10" text-anchor="middle">180° OPEN</text>
  <rect x="970" y="365" width="80" height="160" rx="18" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="1010" y="450" fill="#38bdf8" font-family="monospace" font-size="10" text-anchor="middle">180° OPEN</text>

  <!-- CALLOUT TABLE -->
  <rect x="50" y="550" width="1100" height="170" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="70" y="578" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">SUB-ASSEMBLY 05 HOW THE SPLIT-SADDLE HINGE & LATCH WORK:</text>
  <text x="70" y="604" fill="#e2e8f0" font-family="monospace" font-size="12">[1] CNC Hinge Brackets (saddle_180_pivot_hinge.dxf) clamp directly onto the ø30mm inner carbon tubes so the seat rises with the lift.</text>
  <text x="70" y="628" fill="#fef08a" font-family="monospace" font-size="12">[2] During walking or backing up to the toilet, both saddle halves swing 180° flush against the side tubes (430mm unobstructed hip entry).</text>
  <text x="70" y="652" fill="#22c55e" font-family="monospace" font-size="12">[3] When Grandma wants to sit or transfer, swing the two halves inward: the N52 magnets (20x5mm) pull the twin 10mm 304-stainless conical</text>
  <text x="70" y="676" fill="#22c55e" font-family="monospace" font-size="12">    shear pins into mating tapered sockets (1,200 kgf vertical shear capacity) and trigger the reed switch so firmware knows the seat is locked.</text>
'''
    svg += svg_footer(
        ("HYGIENE & TRANSFER ADVANTAGE: Zero Canvas Slings or Leg Straps to Thread",
         "Wipe-clean antibacterial marine vinyl over closed-cell EVA foam; takes 2 seconds to swing closed."),
        ("SAFETY INTERLOCK: Reed Switch + 4x 50kg Strain Gauges (HX711)",
         "Firmware verifies latch closure and detects >15kg seated weight to auto-lock rear wheels.")
    )
    with open(os.path.join(BP_DIR, "blueprint_05_split_saddle_180_hinge_and_latch.svg"), "w") as f:
        f.write(svg)


def make_sheet_06():
    svg = svg_header(
        "BLUEPRINT 06: MGN9C KITCHEN TRAY, ANTI-BIND FLOAT & ESP32-S3 WIRING",
        "6",
        "Upper Halo MGN9C 300mm Slide-Bridge Tray + Floating Delrin Mount + Complete 24V LiFePO4 / ESP32-S3 / UWB / LiDAR Pinout"
    )
    svg += '''
  <!-- LEFT PANEL: MGN9C SLIDE-BRIDGE TRAY & FLOATING DELRIN MOUNT -->
  <text x="45" y="115" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">[A] UPPER HALO MGN9C TRAY & ANTI-BIND FLOAT</text>
  <rect x="45" y="135" width="520" height="275" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>

  <!-- Left Fixed Mount vs Right Floating Delrin Mount (+-1.5mm) -->
  <circle cx="120" cy="280" r="24" fill="#1e3a8a" stroke="#38bdf8" stroke-width="2"/>
  <text x="120" y="325" fill="#38bdf8" font-family="monospace" font-size="10" text-anchor="middle">LEFT: FIXED CLAMP</text>

  <rect x="435" y="256" width="58" height="48" rx="12" fill="#166534" stroke="#22c55e" stroke-width="2"/>
  <circle cx="464" cy="280" r="18" fill="#0284c7" stroke="#ffffff" stroke-width="2"/>
  <text x="464" y="325" fill="#22c55e" font-family="monospace" font-size="10" font-weight="bold" text-anchor="middle">RIGHT: +-1.5mm DELRIN FLOAT</text>
  <text x="464" y="340" fill="#94a3b8" font-family="monospace" font-size="9" text-anchor="middle">(Prevents Parallel Tube Binding!)</text>

  <!-- MGN9C Linear Rails + 6mm Polycarbonate Tray -->
  <rect x="110" y="220" width="20" height="45" fill="#94a3b8"/>
  <rect x="454" y="220" width="20" height="45" fill="#94a3b8"/>
  <rect x="95" y="190" width="395" height="28" rx="6" fill="#06b6d4" stroke="#cffafe" stroke-width="2"/>
  <text x="292" y="208" fill="#0f172a" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle">6mm LEXAN KITCHEN TRAY ON DUAL MGN9C RAILS</text>
  <text x="292" y="175" fill="#22d3ee" font-family="monospace" font-size="11" text-anchor="middle">Slides 300mm Forward Over Kitchen Counter / Sink</text>

  <!-- RIGHT PANEL: COMPLETE ESP32-S3 & 24V POWER WIRING SCHEMATIC -->
  <text x="595" y="115" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold">[B] MASTER ELECTRONICS & PINOUT SCHEMATIC</text>
  <rect x="595" y="135" width="560" height="585" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5"/>

  <!-- 24V LiFePO4 Battery + E-Stop + Buck -->
  <rect x="620" y="160" width="230" height="75" rx="6" fill="#166534" stroke="#22c55e" stroke-width="2"/>
  <text x="735" y="185" fill="#ffffff" font-family="monospace" font-size="12" font-weight="bold" text-anchor="middle">24V 6Ah LiFePO4 BATTERY</text>
  <text x="735" y="205" fill="#dcfce7" font-family="monospace" font-size="10" text-anchor="middle">+ 30A Fuse + Red Mushroom E-Stop</text>
  <text x="735" y="222" fill="#fde047" font-family="monospace" font-size="10" text-anchor="middle">-> 24V Bus & 5V/5A Buck Converter</text>

  <!-- Central ESP32-S3-DevKitC-1 MCU -->
  <rect x="740" y="285" width="260" height="220" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2.5"/>
  <text x="870" y="312" fill="#38bdf8" font-family="monospace" font-size="14" font-weight="bold" text-anchor="middle">ESP32-S3-DevKitC-1</text>
  <text x="755" y="338" fill="#e2e8f0" font-family="monospace" font-size="11">GPIO 4,5   -> Left Lift PWM (BTS7960)</text>
  <text x="755" y="358" fill="#e2e8f0" font-family="monospace" font-size="11">GPIO 6,7   -> Right Lift PWM (BTS7960)</text>
  <text x="755" y="378" fill="#22c55e" font-family="monospace" font-size="11">GPIO 15,16 -> Left/Right Hall Encoders</text>
  <text x="755" y="398" fill="#fef08a" font-family="monospace" font-size="11">GPIO 17,18 -> Dual 6.5" Hub FOC UART</text>
  <text x="755" y="418" fill="#38bdf8" font-family="monospace" font-size="11">GPIO 8,9   -> I2C (BNO085 IMU + VL53L1X)</text>
  <text x="755" y="438" fill="#f43f5e" font-family="monospace" font-size="11">GPIO 10,11 -> HX711 Seat Load Cells</text>
  <text x="755" y="458" fill="#a855f7" font-family="monospace" font-size="11">GPIO 1,2   -> Handle FSR406 Grip ADC</text>
  <text x="755" y="478" fill="#22d3ee" font-family="monospace" font-size="11">UART1/2    -> LD19 LiDAR + DW3000 UWB</text>

  <!-- Bottom Left Box: Pre-Power Safety Checklist -->
  <rect x="45" y="430" width="520" height="290" rx="8" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
  <text x="65" y="458" fill="#22c55e" font-family="monospace" font-size="14" font-weight="bold">[C] FINAL COMMISSIONING & SAFETY CHECKLIST:</text>
  <text x="65" y="486" fill="#e2e8f0" font-family="monospace" font-size="11">1. Run `python3 firmware/test_safety_interlocks.py` (all 12 tests PASS).</text>
  <text x="65" y="510" fill="#e2e8f0" font-family="monospace" font-size="11">2. Verify Left & Right 24V actuators stay within +-1.5mm across full 300mm</text>
  <text x="65" y="528" fill="#e2e8f0" font-family="monospace" font-size="11">   stroke (active Hall PID auto-levels any weight imbalance).</text>
  <text x="65" y="552" fill="#fef08a" font-family="monospace" font-size="11">3. Place 20 kg test weight on saddle: confirm rear 6.5" hub wheels lock</text>
  <text x="65" y="570" fill="#fef08a" font-family="monospace" font-size="11">   instantly (40 Nm holding torque) and UWB Auto-Summon is blocked.</text>
  <text x="65" y="594" fill="#38bdf8" font-family="monospace" font-size="11">4. Test VL53L1X downward cliff sensor over a 45mm step edge: confirm</text>
  <text x="65" y="612" fill="#38bdf8" font-family="monospace" font-size="11">   wheels halt immediately before the front casters reach the drop-off.</text>
  <text x="65" y="636" fill="#22c55e" font-family="monospace" font-size="11">5. Press Grandma's UWB Summon Pendant from 5m away through a doorway:</text>
  <text x="65" y="654" fill="#22c55e" font-family="monospace" font-size="11">   confirm walker navigates at 0.35 m/s and docks 50cm in front of knees.</text>

  <!-- UWB + LiDAR Callout inside Right Panel -->
  <rect x="620" y="535" width="510" height="160" rx="6" fill="#1e1b4b" stroke="#818cf8" stroke-width="1.5"/>
  <text x="875" y="562" fill="#c7d2fe" font-family="monospace" font-size="13" font-weight="bold" text-anchor="middle">AUTONOMOUS UWB + 360° LiDAR SUMMON MODULE</text>
  <text x="635" y="588" fill="#e2e8f0" font-family="monospace" font-size="11">- 2x MaUWB_ESP32S3 (Qorvo DW3000) Anchors spaced 440mm apart on Upper Halo</text>
  <text x="635" y="610" fill="#e2e8f0" font-family="monospace" font-size="11">- 1x Wearable Pendant on Grandma's wrist/neck (1-button Summon trigger)</text>
  <text x="635" y="632" fill="#e2e8f0" font-family="monospace" font-size="11">- PD AoA Heading + LD19 360° LiDAR doorway centering (fits 510mm doors)</text>
  <text x="635" y="654" fill="#22c55e" font-family="monospace" font-size="11">- Stops at d = 0.50m in front of Grandma, rotates 180°, and locks brakes!</text>
'''
    svg += svg_footer(
        ("ANTI-BIND GUARANTEE: +-1.5mm Floating Delrin Sleeve on Right Upper Halo Joint",
         "Eliminates hyperstatic portal frame binding even if hand-gluing angle varies by +-0.5°."),
        ("FIRMWARE READY: Flash firmware/elderstep_controller/elderstep_controller.ino",
         "Includes all 12 hardware-in-the-loop safety interlocks out of the box.")
    )
    with open(os.path.join(BP_DIR, "blueprint_06_kitchen_tray_and_electronics_wiring.svg"), "w") as f:
        f.write(svg)


def make_interactive_html():
    html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ElderStep Pro — Interactive CAD Assembly Blueprints & Exploded Viewer</title>
  <style>
    :root {
      --bg: #0b1120;
      --panel: #0f172a;
      --border: #334155;
      --cyan: #38bdf8;
      --green: #22c55e;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --text: #e2e8f0;
      --muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      padding: 20px;
    }
    header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: var(--panel);
      border: 1.5px solid var(--cyan);
      padding: 16px 24px;
      border-radius: 10px;
      margin-bottom: 18px;
    }
    h1 { font-size: 20px; color: var(--cyan); }
    .sub { font-size: 12px; color: var(--muted); margin-top: 4px; }
    .badge {
      background: #064e3b;
      color: #6ee7b7;
      border: 1px solid var(--green);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: bold;
    }
    .controls {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
      background: var(--panel);
      border: 1px solid var(--border);
      padding: 16px;
      border-radius: 10px;
      margin-bottom: 18px;
    }
    .ctrl-box label {
      display: block;
      font-size: 12px;
      color: var(--cyan);
      margin-bottom: 6px;
      font-weight: bold;
    }
    input[type="range"] { width: 100%; accent-color: var(--cyan); cursor: pointer; }
    .tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }
    .tab-btn {
      background: var(--panel);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 10px 14px;
      border-radius: 8px;
      cursor: pointer;
      font-family: inherit;
      font-size: 12px;
      transition: 0.15s;
    }
    .tab-btn.active, .tab-btn:hover {
      background: #1e3a8a;
      border-color: var(--cyan);
      color: #fff;
      font-weight: bold;
    }
    .viewer-box {
      background: var(--panel);
      border: 1.5px solid var(--border);
      border-radius: 10px;
      padding: 16px;
      text-align: center;
      overflow-x: auto;
    }
    canvas {
      background: #090d16;
      border: 1px solid #1e293b;
      border-radius: 8px;
      max-width: 100%;
    }
    .sheet-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 24px;
      margin-top: 24px;
    }
    .sheet-card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px;
    }
    .sheet-card h2 {
      font-size: 15px;
      color: var(--cyan);
      margin-bottom: 10px;
    }
    .sheet-card img {
      width: 100%;
      height: auto;
      border-radius: 6px;
      border: 1px solid #1e293b;
    }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>ELDERSTEP PRO (9.85 kg STANDARD-COTS EDITION) — MASTER ASSEMBLY BLUEPRINTS</h1>
      <div class="sub">Interactive Exploded Sub-Assembly CAD Viewer + All 6 Printable 1:1 Engineering Blueprint Sheets</div>
    </div>
    <div class="badge">100% STANDARD MULTI-VENDOR COTS | ₹55,200 | 1-WEEKEND BUILD</div>
  </header>

  <div class="controls">
    <div class="ctrl-box">
      <label>EXPLODE SUB-ASSEMBLIES: <span id="expVal">35%</span></label>
      <input type="range" id="explodeSlider" min="0" max="100" value="35" />
    </div>
    <div class="ctrl-box">
      <label>ACTUATOR LIFT STROKE (12° RAKE): <span id="liftVal">120 mm (Saddle: 537 mm)</span></label>
      <input type="range" id="liftSlider" min="0" max="300" value="120" />
    </div>
    <div class="ctrl-box">
      <label>KITCHEN TRAY FORWARD SLIDE: <span id="trayVal">100 mm</span></label>
      <input type="range" id="traySlider" min="0" max="300" value="100" />
    </div>
  </div>

  <div class="viewer-box">
    <canvas id="cadCanvas" width="1120" height="520"></canvas>
  </div>

  <div class="sheet-grid">
    <div class="sheet-card">
      <h2>SHEET 1/6: Master Chassis Orthographic & Kinematic Envelope (495mm Width, 12° Rake)</h2>
      <img src="../hardware/blueprints/blueprint_01_master_frame_orthographic.svg" alt="Blueprint 01" />
    </div>
    <div class="sheet-card">
      <h2>SHEET 2/6: Telescoping Carbon Column (ø35/ø30mm) & Standard 24V 300mm IP65 Actuator Cartridge</h2>
      <img src="../hardware/blueprints/blueprint_02_telescoping_carbon_actuator_column.svg" alt="Blueprint 02" />
    </div>
    <div class="sheet-card">
      <h2>SHEET 3/6: Rear 6.5" (165mm) Sealed IP65 BLDC Hub Wheel & ø16mm D-Axle Dropout</h2>
      <img src="../hardware/blueprints/blueprint_03_rear_65in_hub_wheel_dropout.svg" alt="Blueprint 03" />
    </div>
    <div class="sheet-card">
      <h2>SHEET 4/6: Ultra-Low 74mm Front Twin-Skate Caster Assembly (SKF 51104 + 64mm 82A PU Wheels)</h2>
      <img src="../hardware/blueprints/blueprint_04_front_74mm_twin_skate_caster.svg" alt="Blueprint 04" />
    </div>
    <div class="sheet-card">
      <h2>SHEET 5/6: 180° Split-Saddle Pivot Hinge & N52 + Conical Stainless Shear-Pin Latch (12 kN)</h2>
      <img src="../hardware/blueprints/blueprint_05_split_saddle_180_hinge_and_latch.svg" alt="Blueprint 05" />
    </div>
    <div class="sheet-card">
      <h2>SHEET 6/6: MGN9C Slide-Bridge Kitchen Tray, Floating Delrin Mount & ESP32-S3 Master Wiring</h2>
      <img src="../hardware/blueprints/blueprint_06_kitchen_tray_and_electronics_wiring.svg" alt="Blueprint 06" />
    </div>
  </div>

  <script>
    const canvas = document.getElementById('cadCanvas');
    const ctx = canvas.getContext('2d');
    const expSlider = document.getElementById('explodeSlider');
    const liftSlider = document.getElementById('liftSlider');
    const traySlider = document.getElementById('traySlider');

    function draw() {
      const exp = parseFloat(expSlider.value) / 100.0;
      const lift = parseFloat(liftSlider.value);
      const tray = parseFloat(traySlider.value);

      const saddleH = Math.round(420 + lift * 0.978);
      const fwdShift = Math.round(lift * 0.208);
      document.getElementById('expVal').textContent = Math.round(exp * 100) + '%';
      document.getElementById('liftVal').textContent = `${lift} mm (Saddle: ${saddleH} mm, +${fwdShift} mm FWD)`;
      document.getElementById('trayVal').textContent = `${tray} mm`;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw Blueprint Grid
      ctx.strokeStyle = '#1e293b';
      ctx.lineWidth = 1;
      for (let x = 0; x < canvas.width; x += 25) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += 25) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
      }

      // Floor Line
      const floorY = 465;
      ctx.strokeStyle = '#64748b';
      ctx.setLineDash([6, 4]);
      ctx.beginPath(); ctx.moveTo(40, floorY); ctx.lineTo(1080, floorY); ctx.stroke();
      ctx.setLineDash([]);

      // Explode offsets
      const eWheel = exp * 55;
      const eCaster = exp * 50;
      const eAct = exp * 75;
      const eTop = exp * 45;

      // 1. Rear 6.5" Sealed BLDC Hub Wheel
      const rx = 220 - eWheel;
      const ry = floorY - 52 + eWheel * 0.3;
      ctx.fillStyle = '#1e293b';
      ctx.strokeStyle = '#f43f5e';
      ctx.lineWidth = 3;
      ctx.beginPath(); ctx.arc(rx, ry, 52, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#38bdf8';
      ctx.beginPath(); ctx.arc(rx, ry, 8, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#f43f5e';
      ctx.font = '11px monospace';
      ctx.fillText('6.5" IP65 Hub Wheel (ø16mm D-Axle)', rx - 80, ry + 72);

      // 2. Rear 7075-T6 Dropout + Carbon U-Base Leg
      ctx.fillStyle = '#334155';
      ctx.strokeStyle = '#e2e8f0';
      ctx.lineWidth = 2;
      ctx.fillRect(230, floorY - 56, 310, 14);
      ctx.strokeRect(230, floorY - 56, 310, 14);

      // Front LiFePO4 Battery Ballast
      ctx.fillStyle = '#166534';
      ctx.strokeStyle = '#22c55e';
      ctx.fillRect(445, floorY - 78, 75, 22);
      ctx.strokeRect(445, floorY - 78, 75, 22);
      ctx.fillStyle = '#dcfce7';
      ctx.fillText('24V LiFePO4', 450, floorY - 63);

      // 3. Front 74mm Low-Profile Twin 64mm Skate Caster
      const cx = 555 + eCaster;
      const cy = floorY - 22 + eCaster * 0.25;
      ctx.fillStyle = '#1e293b';
      ctx.strokeStyle = '#22c55e';
      ctx.lineWidth = 2.5;
      ctx.beginPath(); ctx.arc(cx, cy, 22, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.fillStyle = '#22c55e';
      ctx.fillText('74mm Skate Caster + 51104 Bearing', cx - 60, cy + 40);

      // 4. 12-Deg Base Lug + Outer ø35mm Carbon Barrel
      const bx = 375, by = floorY - 56;
      const rakeRad = 12 * Math.PI / 180;
      const colLen = 185;
      const tx = bx + Math.sin(rakeRad) * colLen;
      const ty = by - Math.cos(rakeRad) * colLen;

      ctx.strokeStyle = '#475569';
      ctx.lineWidth = 20;
      ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(tx, ty); ctx.stroke();

      // Delrin Bushings (exploded slightly upward along axis)
      const dx = tx + Math.sin(rakeRad) * (eAct * 0.4);
      const dy = ty - Math.cos(rakeRad) * (eAct * 0.4);
      ctx.fillStyle = '#22c55e';
      ctx.beginPath(); ctx.arc(dx, dy, 11, 0, Math.PI * 2); ctx.fill();
      ctx.fillText('Lathe-Turned Delrin Bushing + O-Ring', dx + 18, dy + 4);

      // 5. Inner ø30mm Carbon Plunger + Standard 24V 300mm Actuator Cartridge
      const liftPx = lift * 0.45 + eAct;
      const px = tx + Math.sin(rakeRad) * liftPx;
      const py = ty - Math.cos(rakeRad) * liftPx;

      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 13;
      ctx.beginPath();
      ctx.moveTo(bx + Math.sin(rakeRad) * (40 + eAct * 0.5), by - Math.cos(rakeRad) * (40 + eAct * 0.5));
      ctx.lineTo(px, py);
      ctx.stroke();

      // Internal Standard 24V Actuator Cartridge Callout (shown offset in exploded mode)
      const ax = 790, ay = 260;
      ctx.fillStyle = '#0f172a';
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.5;
      ctx.fillRect(680, 40, 410, 380);
      ctx.strokeRect(680, 40, 410, 380);
      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 13px monospace';
      ctx.fillText('EXPLODED COLUMN CARTRIDGE DETAIL:', 700, 68);
      ctx.font = '11px monospace';
      ctx.fillStyle = '#e2e8f0';
      ctx.fillText('• Outer Tube: ø35x31mm 3K Carbon (460mm)', 700, 95);
      ctx.fillText('• Guide: 2x CNC Turned POM (Delrin) Sleeves', 700, 118);
      ctx.fillText('• Inner Tube: ø30x26mm 3K Carbon (440mm)', 700, 141);
      ctx.fillStyle = '#fef08a';
      ctx.fillText('• Core: Standard 24V 300mm IP65 Inline Actuator', 700, 164);
      ctx.fillText('  pinned at top & bottom via 2x M8 Clevis Pins', 700, 184);
      ctx.fillStyle = '#22c55e';
      ctx.fillText('• Zero side-load on actuator; swaps in 3 mins!', 700, 210);
      ctx.fillStyle = '#38bdf8';
      ctx.fillText(`• Current Lift: ${lift}mm / 300mm (Saddle: ${saddleH}mm)`, 700, 240);
      ctx.fillText(`• Kitchen Tray Extension: +${tray}mm forward`, 700, 262);
      ctx.fillStyle = '#f43f5e';
      ctx.fillText('• Total Mass: 9.85 kg | Cost: ₹55,200', 700, 290);

      // 6. 180-Deg Split Saddle on Inner Plunger
      const sx = px - Math.sin(rakeRad) * 45;
      const sy = py + Math.cos(rakeRad) * 45;
      ctx.fillStyle = '#f59e0b';
      ctx.strokeStyle = '#fef08a';
      ctx.lineWidth = 2;
      ctx.fillRect(sx - 85 - eTop * 0.4, sy - 8, 82, 16);
      ctx.strokeRect(sx - 85 - eTop * 0.4, sy - 8, 82, 16);
      ctx.fillStyle = '#fef08a';
      ctx.fillText(`180° Split Saddle (${saddleH}mm)`, sx - 235 - eTop * 0.4, sy + 4);

      // 7. Upper Halo + MGN9C Slide-Bridge Kitchen Tray
      const hx = px;
      const hy = py - eTop;
      ctx.fillStyle = '#334155';
      ctx.strokeStyle = '#38bdf8';
      ctx.fillRect(hx - 20, hy - 12, 135, 12);
      ctx.strokeRect(hx - 20, hy - 12, 135, 12);

      const trayPx = tray * 0.35;
      ctx.fillStyle = '#06b6d4';
      ctx.fillRect(hx + 10 + trayPx, hy - 24 - eTop * 0.3, 130, 9);
      ctx.fillStyle = '#22d3ee';
      ctx.fillText(`MGN9C Kitchen Tray (+${tray}mm)`, hx + 10 + trayPx, hy - 32 - eTop * 0.3);
    }

    expSlider.addEventListener('input', draw);
    liftSlider.addEventListener('input', draw);
    traySlider.addEventListener('input', draw);
    draw();
  </script>
</body>
</html>
'''
    with open(os.path.join(DOCS_DIR, "assembly_blueprints.html"), "w") as f:
        f.write(html)


def make_markdown_manual():
    md = '''# ElderStep Pro (`9.85 kg` Standard-COTS Edition): Master Assembly Blueprints (Sheets 1–6)

All 6 engineering assembly blueprints below are scaled for the **100% Standard Multi-Vendor COTS Cartridge Architecture** (`₹55,200` total cost, `9.85 kg` total mass, `10–12 hour` single-weekend build).

You can also open the interactive exploded CAD blueprint viewer in your browser at [`docs/assembly_blueprints.html`](../docs/assembly_blueprints.html).

---

## Sheet 1 of 6: Master Chassis Orthographic & Kinematic Envelope
![Blueprint 01: Master Frame Orthographic](./blueprints/blueprint_01_master_frame_orthographic.svg)

* **Outer Width:** Fixed **`495.0 mm (19.5")`** — clears every `510 mm (20.0")` Indian bathroom doorway with zero width-morphing motors.
* **Inside Hip/Toilet Clearance:** **`430.0 mm (17.0")`** — backs directly over standard Indian & Western commodes.
* **Front Under-Bed Nose Height:** **`74.0 mm (2.9")`** — slides under low beds and sofas.
* **$12.0^\circ$ Forward-Inclined Columns:** `300 mm` stroke produces **`+293 mm` vertical lift** (`420 mm` $\rightarrow$ `713 mm` saddle height) and **`+62 mm` natural forward weight shift** ("Nose-Over-Toes" biomechanics).

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
'''
    with open(os.path.join(BASE_DIR, "ASSEMBLY_BLUEPRINTS.md"), "w") as f:
        f.write(md)


if __name__ == "__main__":
    make_sheet_01()
    make_sheet_02()
    make_sheet_03()
    make_sheet_04()
    make_sheet_05()
    make_sheet_06()
    make_interactive_html()
    make_markdown_manual()
    print("Generated all 6 SVG Assembly Blueprints, Interactive HTML5 Viewer, and Markdown Manual successfully!")
