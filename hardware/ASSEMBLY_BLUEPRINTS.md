# P0-B1 drawing and fabrication status

[The P0-B1 package](p0b1/README.md) now contains editable CadQuery solid source,
three STEP assembly poses,28 custom STEP parts,13 bored plate DXFs, a dimensioned
A3 review pack, stock nesting,60-row India procurement BOM and assembly/weld map.

**Issue status is engineering review, not fabrication approval.** Purchased parts
are our own interface envelopes. OEM configuration, caster revision, matched guide
fit, weld/bolt/thread calculations, sensor/limit brackets, final guards and electrical
schematic remain [explicit holds](p0b1/RELEASE_HOLDS.csv).

The assembly uses a secured ballast pan and manually indexed screw props. It has
no human seat, sling or walking interface. No occupied movement or human lift test.
The complete [assembly sequence](p0b1/ASSEMBLY_PLAN.md) and
[dummy test protocol](p0b1/BENCH_TEST_PLAN.md) accompany the drawings.

The original STEP model and archived parallelogram/carbon drawings are historical
references and must not be combined with this revision. Retired root generators
remain disabled; use `hardware/p0b1/cad/build.py` for the new source.
