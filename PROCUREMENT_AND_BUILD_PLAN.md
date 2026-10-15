# P0-B1 procurement and build plan

Use the [India build review package](hardware/p0b1/README.md),
[60-row BOM](hardware/INDIA_BOM_SOURCING.csv),
[dated India selections and prepared RFQ](hardware/p0b1/procurement/INDIA_SELECTION.md),
[cutlist](hardware/p0b1/cutlist.csv) and
[assembly plan](hardware/p0b1/ASSEMBLY_PLAN.md).

Actual selections include LINAK LA40PL matched OEM kit, HGR25/HGW25CC guide,
Blickle744589 casters, Pilz751103 relay and TI TPS3431EVM. India sales channels
are identified; key components remain RFQ. Four listing-price rows totalINR16413.15
with mixed tax bases, not a build total. Missing prices are blank, not zero.
Custom steel alone is about152kg nominal, before OEM parts, welds and guards.

Order: supplier drawings and quotes -> H01-H06 structural/fit review -> released
cutting/weld/machining -> mechanical dry-fit -> final stops/guard/electrical
integration -> unloaded commissioning -> reviewed dummy stages. No human use.
No parts ordered, supplier messages sent, stock reserved or physical tests performed.

The CAD source and generated files are a single review revision; they are not
certified fabrication drawings. The [hold register](hardware/p0b1/RELEASE_HOLDS.csv)
identifies exactly what is still needed before cutting or powered motion.
Historical carbon cutlists/BOMs are retired and must not be used for this build.
