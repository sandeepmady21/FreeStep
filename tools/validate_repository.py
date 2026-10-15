#!/usr/bin/env python3
"""Check active repository consistency without treating unknown procurement as zero."""
import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []

for path in list(ROOT.glob("*.md")) + list((ROOT / "hardware").glob("*.md")) + list((ROOT / "research").glob("*.md")):
    text = path.read_text()
    for link in re.findall(r"\]\(([^)]+)\)", text):
        target = link.split("#")[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        target = unquote(target.strip("<>"))
        if not (path.parent / target).exists():
            errors.append(f"Broken local link in {path.relative_to(ROOT)}: {target}")

config = (ROOT / "firmware/elderstep_controller/bench_config.h").read_text()
if not re.search(r"constexpr bool BENCH_COMMISSIONED\s*=\s*false\s*;", config):
    errors.append("Supplied bench configuration must remain uncommissioned")
pins = (ROOT / "firmware/elderstep_controller/board_pins.h").read_text()
assignments = re.findall(r"(\w+)\s*=\s*(\d+)", pins)
values = [int(v) for _, v in assignments]
valid = set(range(0, 22)) | set(range(26, 49))
avoid = {0, 3, 19, 20, 45, 46} | set(range(26, 38))
if len(values) != len(set(values)) or any(v not in valid or v in avoid for v in values):
    errors.append("Duplicate, nonexistent, reserved, USB or strapping board pins")
if dict(assignments).get("position") != "1":
    errors.append("Position sensor must use the documented ADC1 GPIO1")
sketch = (ROOT / "firmware/elderstep_controller/elderstep_controller.ino").read_text()
if any(s in sketch for s in ("PIN_HUB", "runAutoSummonStep", "analogWrite(", "attachInterrupt(")):
    errors.append("Retired drivetrain/incremental-lift control found in active sketch")

rows = list(csv.DictReader((ROOT / "hardware/INDIA_BOM_SOURCING.csv").open()))
ids = set()
known_cost = Decimal(0)
known_mass = Decimal(0)
unknown_cost = unknown_mass = 0
for row in rows:
    ident = row["Item_ID"]
    if ident in ids:
        errors.append(f"Duplicate BOM ID {ident}")
    ids.add(ident)
    try:
        qty = Decimal(row["Qty"])
        if not qty.is_finite() or qty <= 0 or qty != qty.to_integral_value():
            raise ValueError("quantity")
        if row["Installed"] not in ("0", "1"):
            raise ValueError("installed flag")
        for field in ("Unit_Cost_INR", "Unit_Mass_g"):
            value = row[field].strip()
            if value:
                numeric = Decimal(value)
                if not numeric.is_finite() or numeric < 0:
                    raise ValueError(field)
                if field == "Unit_Cost_INR":
                    known_cost += qty * numeric
                    if not row["SKU_Or_Quote"] or not row["Quote_Date"]:
                        errors.append(f"{ident}: price needs quote reference and date")
                elif row["Installed"] == "1":
                    known_mass += qty * numeric
            elif field == "Unit_Cost_INR":
                unknown_cost += 1
            elif row["Installed"] == "1":
                unknown_mass += 1
    except (InvalidOperation, ValueError):
        errors.append(f"Invalid BOM quantity/value in {ident}")

print(f"BOM: {len(rows)} procurement rows")
if unknown_cost:
    print(f"Cost INCOMPLETE: {unknown_cost} unquoted rows; known subtotal INR {known_cost}; total unavailable")
else:
    print(f"Quoted development procurement total INR {known_cost}; review tax/freight notes")
if unknown_mass:
    print(f"Device mass INCOMPLETE: {unknown_mass} unknown installed masses; known subtotal {known_mass} g; total unavailable")
else:
    print(f"Recorded installed mass {known_mass} g; verify assembled device by measurement")
if not rows:
    errors.append("Empty procurement register")
if errors:
    raise SystemExit("\n".join(errors))
print("Active links, pin map, disabled defaults and procurement schema checked")
print("No physical safety, procurement completeness or fabrication approval is implied")
