# P0-B1 bench-test procedure and blank acceptance record

Nothing in this file has been physically tested. Stage masses and limits below
are proposed engineering screening conditions; the test lead must approve them
or replace them with justified values before each stage. No human ballast, body
support trial, occupied movement, cooking, flame, hot liquid or walking.

## Facility and instruments

Use a guarded2.5 x2.5m clear test cell, controlled access, level dry concrete floor,
verified floor capacity and E-stop accessible from outside. Test-cell posts are
independent of the apparatus. External slack recovery rig must have documented
capacity for complete moving structure plus ballast, positioned to arrest before
hazardous drop without hiding frame instability. Record its slack and every contact.
No overhead rig preload during stability tests; restraining catch tethers may arrest
failure but may not provide normal support. No one inside during motion or loading.
Park and isolate mechanically before personnel enter to change ballast or props.

Required: calibrated scale, suitable load cell, travel scale/dial indicator,
independent angle gauge, force gauge, clamp/current instrument and oscilloscope
with safe isolated probes. Log firmware hash, CAD rev, actual BOM serials, floor,
fixture, actuator duty/temperature and wiring schematic rev on every test sheet.

## Sequential gates and proposed criteria

| ID | Setup and action | Proposed predeclared criterion |
| --- | --- | --- |
| B01 | Static dimensional audit, no power | every supplier/machining hold closed; bores, screw exposure, pin stack and all bolt torques recorded |
| B02 | Carriage supported by rated hoist; guide travel by fixture | no binding or steel collision over250mm; >=3mm cap/tab-to-relieved-bridge clearance; vendor face tolerances met |
| B03 | Outputs to lamps only; default disabled | no motion requests at boot/reset/fault; verify both independent stop paths |
| B04 | Watchdog held HIGH, LOW and disconnected with forced command contact | latched stop; watchdog response<=230ms plus documented interface delay; no auto restart; measure physical stop later |
| B05 | No added ballast, closed cell | deliberate reset, <=8sec jogs, independent limits stop before P17; proposed >=1mm residual gap to P17 at stopping worst case; adjust limit placement from measured stopping travel |
| B06 | Position calibration at11 points and linkage disconnect | <=2mm error across stroke; all wiring rail/open faults stop; mechanical disconnect detected by independent limit/cross-check, not assumed from ADC |
| B07 | Release buttons and every stop source atlow/mid/high | proposed total run-on<=5mm; no rebound/drop or restart; if exceeded revise limits/guard envelope and re-review |
| B08 | Engage props atlow/mid/high; transfer using OEM manual lowering | both contact evenly; <=1mm seating drop; no pin pull under load; screw projection14..20; successful <=3mm retraction transfer back |
| B09 | Power-loss recovery atlow/mid/high | frame remains supported; controlled manual lowering; no free release; independent recovery hoist procedure works |
| B10 | Stationary75kg study ballast on props, power removed | proposed30min dwell; <=1mm displacement after initial seating; no visible cracking or loose fastener; not a proof-load test |
| B11 | Off-centre ballast, one-prop retention fixture | reviewed load applied remotely; instrument deflection and recover; acceptance values from H07; no deliberate pin removal under live suspended load |
| B12 |100N remote horizontal challenge at1m height in4 directions | no caster lift or slide>2mm on specified floor; tethers stay slack; stop at first loss of contact; not a human reach allowance |
| B13 |20 cycles per released mass stage within OEM duty cycle | no drift>2mm baseline, loose fastener, new binding or damage; log duty/heat; not endurance qualification |

Suggested added ballast stages:0,5,10,25,50,75kg. **Moving steel already weighs
substantially more than zero:** use generated mass only for planning, weigh the
assembly before any loaded release. Stage0 means no ADDED ballast, not zero lift
load. Every stage requires H05-H10 review, static retention first, then lift/descent
and recovery, then off-centre cases only if prior cases pass.75kg is an analysis
study ceiling, not a declared safe load. No automatic escalation when a test passes.

Secure a rigid ballast crate to four P07 eyes with two independent rated restraints;
put calibrated masses low inside it, no loose water containers or piled weights.
Start symmetric X0/Y700, then reviewed offsets up to X+/-150/Y+/-100mm. Mark actual
centre of mass. Remote forces use a low-friction calibrated pull line; nobody pulls
from inside the cell. Inspect fasteners/welds and compare indicator zero after each
load increase. Stop on sound, binding, crack, leakage, creep, pin seizure, tilt,
unexpected motion, limit mismatch or tether contact. Isolate and use recovery rig.

## Test record (copy one per case/condition)

| Field | Value |
| --- | --- |
| Test ID / stage / date / operator / reviewer | UNTESTED |
| CAD / firmware hash / schematic / BOM serials | |
| Actual moving assembly mass / added ballast / CG | |
| Floor / caster orientation / contact coordinates / tethers | |
| Calibration IDs / instrument ranges | |
| Predeclared acceptance limits / reviewed load | |
| Measured travel / force / current / stop delay / displacement | |
| Raw log / photo / scope trace path | |
| Pass or fail / anomaly / disposition | UNTESTED |
| Signature releasing next stage | NOT RELEASED |

This fixture cannot validate transfer comfort, pressure injury, one-leg clinical
suitability, a human sit-to-stand path, or safe kitchen reach. Those require a later
human-support design and appropriate independent study approval.
