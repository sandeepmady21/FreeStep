# FreeStep P0-B1 — India bench package

Revision P0-B1, 15 October 2026. **Engineering review issue; secured ballast only.**
This package replaces the earlier topology-only P0 documents for mechanical detail.
It is a workshop fixture for testing vertical rise, controlled descent and stationary
perch retention. It is not a patient lift, a human seat, a walking aid or a home product.
No payload rating or fabrication approval is claimed.

## Files and source of truth

- [Editable CadQuery source](cad/build.py), [nominal dimension register](parameters.json), [dependency versions](cad/requirements.txt).
- [Three STEP assembly poses](cad/generated/assemblies), [individual custom STEP parts](cad/generated/parts), [plate DXFs](cad/generated/dxf).
- [Dimensioned drawing pack](drawings/FreeStep_P0B1_review_pack.pdf); numbers govern, never scale the PDF.
- [Complete custom-part manifest](cad/parts_manifest.json), [tube cutlist](cutlist.csv), [procurement BOM](../INDIA_BOM_SOURCING.csv).
- [India sourcing evidence and RFQ](procurement/INDIA_SELECTION.md), [assembly and weld map](ASSEMBLY_PLAN.md).
- [Electrical integration](ELECTRICAL_INTEGRATION.md), [dummy test procedure](BENCH_TEST_PLAN.md), [holds](RELEASE_HOLDS.csv).
- [Generated checks and preliminary calculations](reports/checks.json), [verification source](tests/check_design.py).

All dimensions mm. X is left/right, Y increases toward ballast/user side, Z up.
Floor Z0; caster axes X +/-400, Y0/1000. The steel frame is 930 mm across caster
plates, 1100 mm along the base legs and 1451 mm tall, before guarding, caster
sweep and control-box reservation. A nominal250 mm actuator stroke moves the ballast pan top from
430 to 680 mm. Props have 25 mm index steps plus limited screw adjustment.
Final usable command travel may be shorter after limit/stop-distance calibration.
These heights study pelvis movement; they do not establish a sit-to-stand trajectory.
The pan is rigidly attached, with no sling or human-contact interface.

Purchased shapes are our own simplified **interface/exclusion envelopes**, not
manufacturer CAD. The exact LA40PL configuration, current caster dimensions,
rail end distances, installation tolerances and electrical interfaces must be
confirmed against received components. No claim of complete clash verification
is made for unmodelled pedals, cables, guards or supplier internals.

## Release sequence

1. Resolve H01-H06 before material cutting or production machining. Review this
   entire package with the fabricator and responsible mechanical engineer.
2. Complete approved weld sizes/procedure, independent end-stop design, guard/test
   cell design and supplier fit check before powered motion (H07-H10).
3. Resolve OEM electrical interface and independent stop path before energising;
   prove unloaded operation before applying dummy mass.
4. Release each dummy test stage by recorded review. All physical results are blank.

The BOM is a procurement register, not a basket of all-stock parts. India sales
routes are identified; key OEM parts remain RFQ. Prices are dated listing snapshots,
not quotes or a complete build cost. Do not buy an actuator substitute to bypass
an unavailable OEM configuration. No parts ordered and no supplier messages sent.

## Rebuild

From repository root, Python 3.11+ in a fresh virtual environment:

```sh
python -m pip install -r hardware/p0b1/cad/requirements.txt
python hardware/p0b1/cad/build.py
python hardware/p0b1/tests/check_design.py
python hardware/p0b1/tests/check_exports.py
python hardware/p0b1/cad/build_drawings.py
python firmware/test_safety_interlocks.py
python tools/validate_repository.py
```

The drawing generator uses ReportLab and svglib; no FreeCAD installation is needed.
Sharp-corner tube models overestimate real rolled-section mass/stiffness. Generated
checks are screening calculations and selected solid-intersection checks, not FEA,
fatigue analysis, weld qualification, certification or physical test results.

The JSON is a nominal dimension register, not a fully independent parametric UI.
Some geometry dimensions are explicit in the editable Python source. Edit source
and register together, then regenerate and re-review every derived file.
