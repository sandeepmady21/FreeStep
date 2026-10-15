# India component selection and supplier questions

Checked15 October2026. **Listed in India is not the same as confirmed stock,
compatible configuration, delivered availability or an accepted quotation.** No
purchase, supplier contact or reservation has been made. Sources below distinguish
manufacturer dimensions from reseller price/availability claims. Reconfirm at order.

## Mechanical selection

| Item | Selected part | India route and evidence | Disposition |
| --- | --- | --- | --- |
| Lift | LINAK LA40PL,24V,8000N,250mm stroke, manual lowering and safety nut; matched CBJ2/BAJ/CHJ2/HB70 | [LINAK India](https://www.linak.in/contact/) has Noida OEM sales; explicitly does not supply end users directly | RFQ through approved OEM/integrator; full order code unresolved; do not buy bare actuator |
| Rail | HIWIN HGR25,1000mm, matched to HGW25CC | [Novo3D PRE_HW011](https://novo3d.in/hiwin-hgr25-linear-rail/) shows INR5799 and in stock | Listing snapshot, tax basis unclear; obtain genuine matched kit; reject implausible250g listing mass |
| Blocks |2 HIWIN HGW25CC | [Moglix](https://www.moglix.com/hiwin-84x70x36mm-stainless-steel-linear-guideway-block-hgw25cc/mp/msnekpqerq6y52) lists INR3089 each inclusive tax and AVAILABLE ON REQUEST | No verified immediate stock; supplier match/preload/accuracy needed |
| Castors |4 Blickle LWK-TPA126G-FI-P25,744589 | [Blickle India](https://www.blickle.in/) manufacturer sales route | Exact SKU stock/price RFQ; wheel and swivel lock required |
| Structural steel |80x40x4 and60x60x4 RHS, certified YSt355; S355 plate | [Jindal India hollow sections](https://jindalindia.com/hollow-sections.php) lists applicable grade/standards capability | Exact sizes/grade/stock through local certified stockist; MTC and real section data |
| Pins |EN8/C45 turned12x70 and16x110 | Local precision machine shop, CAD dimensions | Custom fabrication; material evidence and paired bore fit required |
| Prop screws |ISO4017 M20x100-8.8 full thread, coarse2.5 | Certified Indian fastener dealer; [Unbrako](https://www.unbrako.com/) sourcing route | Exact SKU/batch RFQ; partial-thread bolt cannot substitute |

Manufacturer basis: [LINAK LA40 page](https://www.linak.com/products/linear-actuators/la40)
identifies PL as full-stroke8000N; other LA40 versions have different curves. The
manufacturer-authored [LA40 data sheet hosted by Indian dealer](https://www.mechatronicscontrol.com/img/products/linak/123.pdf)
is an older revision: PL drawing0404022 shows retractedS+274 for strokes<=300mm.
It is the524mm provisional CAD basis, not confirmation of a current purchasable code.
Specify upperMLF12.2mm eye, rear end7 with12.2mm bore/28mm width if compatible,
manual loweringML, safety nut/ratchet spline option0L and JUMBO-compatible E1
switching as a configuration REQUEST. OEM must resolve compatibility and provide
current2D/3D drawing, code, force/speed/duty curves, minimum battery condition,
current limits, approved controls, manuals, load retention and recovery.

[HIWIN manufacturer HGW tables](https://www.hiwin.de/en/Products/Linear-guideways/Blocks/Ball-guides/Series-HG-QH/HGW-QHW/c/4376)
and [catalogue](https://www.hiwin.com/wp-content/uploads/Linear_Guideway-E.pdf)
are the source for H36/W70/L84,57x45 M8, C0=52.82kN per block and HGR25 nominal
rail23x22/pitch60/end20. Rail catalogue rating is not device capacity; mounting-face
flatness, moments, block spacing, preload, lubrication and fasteners affect use.
Do not mix an untraceable clone rail with genuine blocks and assume catalogue loads.

Blickle [G16 English manufacturer chapter](https://www.blickle.com.au/-/media/project/blickle/global-web/service/mediathek/katalogkapitel/pdf-dokumente/en/g16-chapter-2.pdf?fh=6b9ea5a680c71ab887a80559b2ce0bf2)
gives125x32 wheel,110kg,163mm height,90x66 plate,75x45 or61x51 holes and40mm offset.
A newer [manufacturer Food & Beverage catalogue](https://katalog.blickle.de/brochure/food-beverage/catalogs/Food-Beverage-Dez25/pdf/complete.pdf)
lists164mm for that family: **H03 must reconcile this1mm discrepancy**. All CAD
uses163mm. If received height164mm, all floor-referenced Z values rise1mm; component
relative geometry stays the same only if all four casters are identical. Record
revision rather than filing parts to compensate.110kg/caster does not validate
load-sharing, tipping or brake force. No vendor pedal model was available here.

## Electrical and instrumentation selection

| Item | Actual selection | India evidence / status |
| --- | --- | --- |
| E-stop | Schneider XB5AS8444,2NC | [Official India eShop](https://eshop.se.com/in/emergency-stop.html); stock/login quotation needed |
| Safety relay | Pilz751103 PNOZs3C24VDC2NO | [RS India1919855](https://in.rsdelivers.com/product/pilz/751103/pilz-pnoz-s3-c-24v-dc-safety-relay-2-safety-1/1919855); RFQ; full schematic needed |
| Limits/proofs | Telemecanique XCKP2118P16,9 units | [Electrihub India](https://electrihub.com/telemecanique-limit-switch-xckp2118p16); listed, stock and actual2D mount drawing unconfirmed |
| Gate interlock | XCSB701 with matched actuator, requested XCSZ01 | [Electrihub India](https://electrihub.in/telemecanique-limit-switch-xcsb701) listing; [manufacturer2NC+1NO data](https://downloads.telemecaniquesensors.com/dam/datasheets/en/XCSB701_EN.pdf); stock/mating key RFQ |
| Absolute position | Gefran LT-M-0250-P,250mm,5kohm | [Rajvi](https://rajviinstruments.com/gefran/) India catalogue; RFQ current drawing/end-overtravel/price |
| MCU | ESP32-S3-DevKitC-1-N8R8 | [Mouser India](https://www.mouser.in/en/ProductDetail/Espressif-Systems/ESP32-S3-DevKitC-1-N8R8?qs=sGAEpiMZZMukLrVqQfzRdxL9qjW4vMrDIgqvB9IpdYjh9HGmSaV2DA%3D%3D) regional page lists stock; confirm checkout/board revision. N8-only page is obsolete/restricted, so not selected |
| IMU | GY521 MPU6050, WV-07016 | [Wavtron](https://www.wavtron.in/products/gy-521-mpu-6050-gyroscope), INR145 inclGST, low stock1; bench module, verify3.3V bus |
| Watchdog | TI TPS3431EVM | [DigiKey India](https://www.digikey.in/en/products/detail/texas-instruments/TPS3431EVM/9686050), stock2, INR4291.15 listing; tax/import/freight terms unconfirmed |
| Auxiliary supply | Mean Well HDR-30-24 plus approved isolated5V branch | [Manufacturer](https://www.meanwell.com/); Indian distributor RFQ; final branch/fuse/capacity review |

Watchdog configuration comes from the [TI data sheet](https://www.ti.com/lit/ds/symlink/tps3431.pdf)
and [EVM user guide](https://www.ti.com/lit/ug/snvu614/snvu614.pdf): preset200ms,
range170..230ms. Do not rely on reseller summaries for switching behaviour.
The motion interface, watchdog latch, sensor conditioning, connector terminals,
ratings and wiring harness still need a released integrator schematic. H09 is a
real powered-build blocker; grouping it in the BOM does not make it finished.

Position conditioning is included in the CONTROL kit: MCP6002-I/P buffer and
explicit passive netlist in ELECTRICAL_INTEGRATION.md. [Microchip data](https://www.microchip.com/en-us/product/MCP6002)
and [Mouser India listing](https://www.mouser.in/en/ProductDetail/Microchip-Technology/MCP6002-I-P?qs=Ux5rHyN1IXStLRM979v6Rg%3D%3D)
support the selected device; no board layout/accuracy is validated yet.

## Procurement economics

The CSV is generated from the CAD manifest plus these selections.60 procurement
rows include all28 custom-part definitions and purchased/services lines; rerun the
script when geometry changes. Only four rows have defensible dated numeric listing
prices: rail, blocks, IMU and watchdog. Their mixed-tax subtotal is INR16413.15,
**not a project budget**. Lift kit, steel, machining, welding, safety integration,
guarding, test equipment, taxes and freight are unquoted. No build-total or lightweight
claim can be supported yet. Weigh the assembled device; generated custom steel alone
is about152kg. This is an intentionally substantial bench fixture, unsuitable for
an ordinary kitchen or stair transport in its present form.

## Ready-to-send RFQ (prepared only; not sent)

Please quote qty1 engineering bench fixture kit for India delivery. Attach this
P0-B1 CAD/drawing/BOM package. State exact manufacturer codes, drawing revisions,
stock location, lead time, MOQ, GST, freight, return policy, certificates, manuals
and exclusions. No unapproved substitutes. Provide written answers to:

1. LINAK integrator: full configuration above,524mm pin-centre fit,12.2mm eye/28mm
   width, self-lock/safety nut, compatible manual descent, current/duty/force,
   approved command-inhibit and health outputs, stopped/welded-output response,
   emergency recovery and warranty for this secured-ballast fixture.
2. Guide supplier: one genuine1000mm HGR25 plus2 HGW25CC matched set, preload and
   accuracy class, actual rail ends and hole locations, mounting tolerances,
   grease/interval, fastener lengths/torques and combined load review.
3. Blickle:744589 exact current height, hole pattern, wheel AND swivel brake,
   pedal envelope and rated floor/loading conditions; India stock and quotation.
4. Fabricator: grade/mill evidence, saw cuts, plate cutting, paired pin machining,
   tapped threads, post-weld guide machining, weld engineering/WPS and inspection.
   Quote separately for engineering, material, machining, welding and finishing.
5. Electrical integrator: final schematic and terminal BOM satisfying the independent
   stop, latching watchdog, no-restart, isolation and directional limit requirements.
   Prove no idle-watchdog deadlock and no single stuck command bypasses stop.

Do not order precision plates/clevises before answersH01-H06. Procurement may begin
with supplier samples and independent fixture review; no stock statement above is
a guarantee of checkout availability.
