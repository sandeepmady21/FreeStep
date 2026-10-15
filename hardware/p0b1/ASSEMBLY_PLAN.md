# P0-B1 assembly and inspection plan

Review issue; no human use. Follow [release holds](RELEASE_HOLDS.csv). All operations
below are planned, not performed. Two people plus appropriate lifting equipment
are required: this fixture is too heavy to treat as a portable household aid.

## Datums, materials and manufacturing notes

A = common top surface of four caster plates, Z171; B = rail mounting face Y140;
C = X0 centre plane. Work from these datums, not accumulated tube tolerances.
S355 plate / certified YSt355 RHS; EN8/C45 pins. Do not silently substitute E250,
thin furniture tube, aluminium, printed clevises or threaded bolts for the pins.
Use actual mill section properties; nominal wall is not guaranteed minimum wall.

Quote square saw cuts +/-0.5 mm; general plate dimensions +/-0.3 mm, hole positions
+/-0.2 mm unless vendor requirements are tighter. These are fabrication targets,
not supplier guide-mount tolerances. Pair-machine actuator ears and ladder plates.
Deburr all edges, break exposed edges R1 minimum. M6 and M12 holes in the model are
tapping pilots, not finished clearance holes. P15 needs a real M20x2.5-6H through
thread, not the 17.5 mm CAD pilot. Gauge threads and measure actual engagement.
P16 has a real underside circular pocket, diameter20.5 x3 deep.
P11 includes a centred 60 x6 mm front-edge relief through all 12 mm thickness.

Weld the backbone/bridge assemblies before final face machining. Do not bolt a
precision rail to an untreated weldment. Quote stress-relief/straightening and
machining as needed to meet the supplied HIWIN installation specification. Mask
guide faces, threads and pin bores during coating. There is no released weld size:
the joint schedule below defines connectivity; engineer to sign weld throat,
length, access, distortion sequence and inspection before fabrication.

## Weld joint schedule (quantity is joint locations)

| Joint | Connection | Locations | Preparation / access |
| --- | --- | ---: | --- |
| W01 | T02 ends to inside faces of T01 | 2 | 760 between base inner faces; jig caster axes first |
| W02 | T01 underside to P01 tops | 4 | RHS must not cover mounting-bolt heads; inspect four holes accessible |
| W03 | T03 bottoms to T02 top | 2 | square to A and C; mast centred Y104 |
| W04 | P02 rear face to T03 rear faces | 2 continuous interfaces | B machined after weld, no rail installed during welding |
| W05 | P13 webs to outside of T03 and base top | 2 | right X110..116, left -116..-110; do not bury web inside tube |
| W06 | P10 to top of T02 | 1 | tap M12 only after weld; removable P04 bolts to this landing |
| W07 | P05 ears to P04 | 2 | pair-bore pin axis after weld; 28.5 inner gap subject to OEM fit |
| W08 | T09 ends to inside face of T01; T08 bottom to T09 top | 2 each | fixed prop posts X+/-330, Y1000; check T09 spans 280..380 on right |
| W09 | P11 bridges to T08 front and rear edges of P08 pair | 4 bridges | retain relief; do not fill clearance notch with weld |
| W10 | T05 front ends to rear face of T04 | 2 | T05 starts Y70; square butt joints |
| W11 | T10 ends to T05 inner faces | 2 | T10 length460; continuous side arms; no intersecting uncut tubes |
| W12 | P12 spacers between P03 rear and T10 front | 2 | spacer Y188..218; finish-machine P03 block face |
| W13 | P06 upper ears to underside T04 | 2 | pin Z854 at retraction; pair-bore and preserve manual-lowering access |
| W14 | T06 tops to T05 undersides | 4 | drops run Z424..884 at lower pose |
| W15 | T06 bottoms to T07 tops | 4 | cross members at Y580/820, top Z424 |
| W16 | P07 to T07 tops | 2 interfaces | restraint holes must remain accessible below; avoid pan distortion |
| W17 | P09 front edges to rear face of rear T07 | 2 | tab underside380, rear edge935; full load-capable joint review required |

P15, P16, pins, rail, bearing blocks and actuator are NOT welded. Retain P16 with
slack non-load-bearing tethers clear of moving members. P15 is removable and
indexes by PIN16 through both ladder walls. No drilling of RHS load paths for
unreviewed mounts. Small brackets, guard posts and OEM mounts are fit-check holds.

## Fasteners and receipt checks

| Joint | Quantity / specified fastener | Verify before choosing length or torque |
| --- | --- | --- |
| Rail to P02 | 17 M6 ISO4762-8.8, tentative20 long | actual counterbore, rail thickness below bolt head, >=9 mm engagement; no bottoming |
| P03 to blocks | 8 M8 ISO4762-8.8, tentative25 long | head-side washers, 12 mm plate; OEM thread depth and torque |
| Caster plates | 16 M8 ISO4017-8.8, tentative30 long; flat washers + all-metal locknuts | actual mounting plate thickness, pedal and tool access, two visible threads |
| Lower clevis | 4 M12 ISO4762-8.8 x30 tentative + washers | through P04; 15+ mm P10 engagement after washer; vendor load calculation |
| Ballast restraint eyes | 4 M10 forged through-bolt eyes, washers/backing and locknuts | rated restraint geometry, eye load directions and clearance under pan |
| Perch props | 2 ISO4017 M20x100-8.8 full thread | full 80 mm threaded block; nominal17 mm exposed; permissible14..20 |
| Pin retention | 8 ISO1234 3x25 split pins + 8 flat pin washers | four pins, two ends each; cross holes5 mm from ends; replace split pins after removal |

Tentative bolt lengths are procurement candidates, NOT permission to fit a bottomed
or too-short bolt. Obtain joint-specific tightening values from HIWIN, Blickle and
the joint engineer; do not use one generic torque for these different interfaces.
Record actual batch, length, coating, torque and torque-tool serial in the build log.

## Assembly sequence

1. Receive components and compare serial/drawing revisions with RFQ; measure
   actuator pin centres, eye widths, rail holes, block pattern and castor height.
   Reject unmatched rail/block sets or missing material/fastener certificates.
2. Dry-jig fixed steel on a flat table; verify diagonals, four plate coplanarity,
   mast square and prop ladder alignment. Tack, inspect, then weld to approved WPS.
3. Machine B and P03 mating face; pair-drill/ream pins and tap pilots. Deburr,
   inspect welds per engineer, protect faces and finish steel. No coating in bores.
4. Install castors; check wheel AND swivel locks at all four locations. Fit guide
   and two blocks to OEM cleanliness, lubrication and bolt sequence. Keep shipping
   retainers until blocks are safely on the rail; support the heavy moving assembly.
5. Jig and weld moving frame separately. Fit bridge to blocks. With a hoist supporting
   the frame and actuator absent, check full250 mm travel for binding and interference.
   Hands remain outside drop/pinch zones. Do not let carriage run off an unretained rail.
6. Fit the approved independent rail-end retention stops (H08), then actuator using
   PIN12 with flat washers and split pins. No side-load or forced alignment. Confirm
   manual lowering is reachable with its supplied tool at all heights.
7. Install ladders, screw blocks, pins, jackscrews and caps; verify correct 25 mm row
   correspondence on both sides. Measure cap-to-bridge clearance throughout travel;
   nominal relief6 mm must leave >=3 mm measured clearance under test deflection.
8. Fit approved ballast restraints, position sensor/link, independent limits, brake
   proofs, enclosure and guarded test cell. These match-drilled interfaces need the
   supplier/fabricator's released detail; CAD envelopes alone do not define them.
9. Complete the signed electrical schematic, independent stops, lockout, fuses and
   commissioning. Begin [unloaded tests](BENCH_TEST_PLAN.md); no ballast before release.

## Perch transfer and recovery (prove first with zero added ballast)

Both props are independent: either must be reviewed for the complete moving load.
Stop at a matching index height; release controls. Insert each PIN16 fully through
both walls and P15, fit both split pins. Adjust screw via its accessible hex head
below P15 until cap approaches tab; exposed screw must remain14..20 mm. Confirm both
pin proofs. Software inhibits BOTH directions when either prop is engaged.

Use the OEM's documented manual lowering, slowly, to seat both tabs on their caps;
nominal transfer is <=1 mm. Isolate motion and measure retention. No electronic
UP command is needed to release the props. To recover, restore the connected,
self-locking OEM support; retract each screw evenly in <=quarter-turn increments,
maximum3 mm total, until the OEM actuator has taken the load and both pins are free.
Never remove a loaded pin or pry a jammed prop. If pins do not become free within
that range, stop and use the independently rated overhead recovery hoist outside
the fixture load path. No person under the suspended assembly.

Remove unloaded props/pins and restore their parked stowage before electrical
lowering. In a power failure, transfer from props as above, then use approved OEM
manual lowering. A free release lever is not an acceptable emergency descent method.
Ratchet spline, manual lowering, safety nut and self-lock behaviour require a
supplier-reviewed combination; if incompatible, revise the design before assembly.
