# P0 procurement and construction plan

**Bench-only development. No fixed cost, mass, one-weekend build duration or
human load rating is asserted.** The active [BOM](hardware/INDIA_BOM_SOURCING.csv)
is a request-for-quote register. Blank prices/masses mean unknown, never zero.

## Order of work

1. Run software checks using existing development equipment. Do not order the
   archived CNC profiles, carbon stock or split-seat latch.
2. Resolve the [prototype specification](hardware/PROTOTYPE_SPEC.md): adult fit,
   seated support access, load/trajectory envelope, mechanical rest lock and
   emergency recovery. Build a non-load-bearing adjustable geometry mock-up.
3. Request matched OEM lift-system quotations and manuals; review their controller
   input contract and permitted use. Obtain supplier confirmation of actuator
   load/duty cycle, self-lock/secondary retention, emergency lowering, travel
   limits, overload/thermal behavior and required inspection/service.
4. Select compatible body-support/seat interfaces with the system engineer and
   clinical adviser. Obtain explicit dimensions and attachment constraints; a
   sling is not universally compatible with arbitrary custom hooks.
5. Issue one reviewed CAD/drawing/BOM revision, including materials, tolerances,
   fasteners, guide moment ratings, guards, weld/bond details if any, and the
   complete electrical safety circuit. Populate a new cutlist from that revision.
6. Construct/commission the unloaded rig under the validation plan. Record
   wiring, calibration, stopping travel and fault-injection results. Only then
   consider dummy loads. Human testing is a separate, currently open release gate.

## Quote and mass records

Use `Unit_Cost_INR` for one listed procurement unit and `Unit_Mass_g` for its
installed unit mass. `Qty` multiplies each. Kits have quantity 1 and a documented
kit composition. `Installed=0` excludes engineering/test equipment from assembled
device mass, but not development cost. Do not count a supplier price without
SKU/quote reference and quote date. Record tax/freight inclusion in `Notes`.

```sh
python3 tools/validate_repository.py
```

This checks quantity and numeric fields, sums known costs/masses, and explicitly
reports an **incomplete** total while any required quote or mass is missing.
It does not infer that unknown items can be bought at the old estimated prices.

## Fabrication status

There is no P0 tube cutlist yet because frame dimensions and guide geometry are
not released. The carbon architecture is retired, so buying one extra carbon tube
would not resolve the design mismatch. For historical audit only, its 30 mm
cutlist required 2,375 mm while the old order contained 2,000 mm; its BOM actually
had 20 rows, ₹54,450 and 9,700 g assuming row-total mass. These are not P0 estimates.

See [drawing status](hardware/ASSEMBLY_BLUEPRINTS.md). Invalid plate STLs are kept
only as archived reference; no production exports are generated from them.
