# P0 drawing and fabrication status

**No P0 fabrication drawings are released.** The original STEP assembly,
parallelogram viewer, carbon column profiles, and split-saddle drawings represent
different historical concepts. They cannot be combined into a P0 build.

The [prototype specification](PROTOTYPE_SPEC.md) contains the current system
diagram. Its topology is one guided lift and passive mechanically locked wheels.
The [wiring guide](WIRING_AND_ASSEMBLY_GUIDE.md) defines the bench signal contract.

Before issuing CAD, record these drawings with part/revision numbers:

1. Adjustable human/seat/worktop/stride envelopes and loaded stability polygon.
2. Base and wheel/swivel-lock assembly with wheel contact coordinates.
3. Guided mast, anti-rotation carriage, actuator alignment and full moment loads.
4. Body-support attachment interfaces and seated application/removal route.
5. Positive perch lock, load-transfer/unlocking mechanism and emergency lowering.
6. Guards, independent travel stops, cable clearances and end-of-travel details.
7. OEM power/safety circuit, monitored interlocks and heartbeat watchdog wiring.

Verify that the STEP, drawings, DXFs, STL exports, cutlist and BOM describe the
same revision. Every bore, thread, counterbore, clamp gap and pocket must have a
defined manufacturing operation; a circle labelled as a pocket does not specify
its depth. Compare section views and physical samples before ordering a batch.

Old generators are archived as reference text. Their STL plate extrusions omitted
holes and their profiles did not encode complete three-dimensional mechanisms.
No replacement geometry is generated until the load path and interfaces are solved.
