# P0-B1 verification record

Executed15 October2026 on the local development host. No physical hardware tests were performed.

- Native firmware:48 core regression cases and5 adapter checks passed with address/undefined-behaviour sanitizers.
- ESP32-S3: PlatformIO target compiled successfully, default commissioning remains false.
- Geometry:18 design assertions passed, including51 travel samples at5mm intervals, rail/stop bore coordinates, indexing and stock nesting.
- Exports:44 round-trip checks passed:28 custom STEP parts,13 plate DXFs and3 STEP assemblies.
- Repository: active Markdown links, pin map, default lockout and CAD/BOM custom-part quantities checked.
- PDF:23 A3 sheets rendered and visually inspected; camera roll corrected to world-Z-up.

These results do not establish load capacity, physical stopping, wiring integrity, fatigue life, clinical suitability or fabrication approval. H01-H10 remain OPEN.

## Source SHA256

- cad/build.py: `80ee09f0beee60e7d5f6c5021d8de841b75bd4adfcfcff879ba021f59942c89e`
- cad/build_drawings.py: `30f8acff5d7dbf0a994b31dd20b184f79a062d7ae379037a6994ca4dde4040fe`
- parameters.json: `3f65b558aad0d9b47d11919e85ee69c0e606b08cfe9354e3de6fcd466b7ededc`
- tests/check_design.py: `db7ab04ea7a0ca93e10d85aa578eaeddb3a4b0b7c4a430868fc1bb589db7804d`
- tests/check_exports.py: `a3dcbfc12092f819323032e572a667c1a3c766fe40a22762b89fba1d3ac25c31`
