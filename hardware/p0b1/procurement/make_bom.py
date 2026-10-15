#!/usr/bin/env python3
"""Merge custom CAD quantities with dated procurement selections; blanks stay unknown."""
from pathlib import Path
import csv,json
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'cad/parts_manifest.json').read_text())
fields=['Item_ID','Part_Description','Qty','Installed','Unit_Cost_INR','Unit_Mass_g','Supplier_Candidate','SKU_Or_Quote','Checked_Date','Notes','Source_URL','Availability','Price_Basis','Selection_Status']
rows=[]
def row(i,d,q,s,sku,url,status,notes='',price='',basis='',installed=1,mass=''):
 rows.append(dict(zip(fields,[i,d,q,installed,price,mass,s,sku,'2026-10-15',notes,url,status,basis,'CONFIRM_BEFORE_ORDER'])))
for p in m['parts']:
 if p['kind']=='custom':
  row(p['id'],p['description'],p['quantity'],'Indian precision fabricator / certified steel stockist',p['id']+' P0-B1','https://jindalindia.com/hollow-sections.php','RFQ; exact stock and fabrication unconfirmed',p['material']+'; nominal CAD mass excludes welds/coating',mass=round(p['unit_mass_kg']*1000,1))
row('LIFT','Matched LA40PL lift kit incl CBJ2 BAJ CHJ2 HB70 cables mounting hardware',1,'LINAK India OEM sales / approved integrator','LA40PL configured 24V 8000N 250mm; full code by OEM','https://www.linak.in/contact/','RFQ; OEM channel; end-user sale not offered','S+274=524mm drawing assumption; ML/safety nut/ratchet spline and emergency controls must be compatible; H01/H02')
row('RAIL','HIWIN HGR25 rail 1000mm',1,'Novo3D','PRE_HW 011 / HGR25R1000','https://novo3d.in/hiwin-hgr25-linear-rail/','Listing says in stock; not reserved','Purchase matched rail+blocks; reject listing 250g mass; verify authenticity and cut end distance',5799,'Listed INR; tax basis unspecified')
row('BLOCK','HIWIN HGW25CC flange block',2,'Moglix','HGW25CC','https://www.moglix.com/hiwin-84x70x36mm-stainless-steel-linear-guideway-block-hgw25cc/mp/msnekpqerq6y52','AVAILABLE ON REQUEST','Matched preload/accuracy/rail lot required; 57x45 M8; vendor nominal mass differs from seller',3089,'Listed inclusive GST; page shows 2622+467; not quote')
row('CASTER','Blickle wheel AND swivel lock plate caster',4,'Blickle India','LWK-TPA 126G-FI-P25 / 744589','https://www.blickle.in/','India sales channel; exact stock RFQ','125x32 wheel; 110kg catalogue per caster not system rating; 163mm assumed vs newer catalogue164mm; reconcile H03')
row('BOLT20','ISO4017 M20x100-8.8 full thread coarse2.5',2,'TVS/Unbrako authorized Indian industrial fastener stockist','ISO4017 M20x100 8.8','https://www.unbrako.com/','RFQ size and batch','Full thread required; 80mm thread engagement,14..20 projection; engineer thread stripping/contact review')
for i,desc,q,sku,note in [
 ('F01','Rail socket screws',17,'ISO4762 M6x20-8.8','Length tentative; OEM torque and engagement required'),
 ('F02','Block socket screws',8,'ISO4762 M8x25-8.8','Length tentative; confirm blind hole depth'),
 ('F03','Caster bolts',16,'ISO4017 M8x30-8.8','Length tentative; washers and all-metal locknuts included separately'),
 ('F04','Clevis-base screws',4,'ISO4762 M12x30-8.8','Length tentative; verify actual engagement'),
 ('F05','M8 flat washers',44,'ISO7089 M8 steel 200HV','8 block +32 caster +4 end stops; final OEM allowance'),
 ('F06','M12 flat washers',4,'ISO7089 M12 steel 200HV','Clevis base'),
 ('F07','M8 all-metal locknuts',16,'ISO7042 M8 class8','Castors; no nylon near heating operations'),
 ('F08','Pin split retainers',8,'ISO1234 3x25','Replace after removal; four pins two ends each'),
 ('F09','Pin end washers dia12',4,'ISO7089 M12 steel','Check retained pin stack against real OEM eyes'),
 ('F10','Pin end washers dia16',4,'ISO7089 M16 steel','Check retained ladder pin stack'),
 ('F11','Retention-stop screws',4,'ISO4762 M8x55-8.8','Length tentative; through36mm stop+washer into16mm backing')]:
 row(i,desc,q,'Certified Indian fastener stockist',sku,'https://www.unbrako.com/','RFQ exact standard/length',note)
row('ESTOP','Two-NC latching twist-release mushroom emergency stop',1,'Schneider Electric India eShop','XB5AS8444','https://eshop.se.com/in/emergency-stop.html','Listed; login/stock and delivered price unconfirmed','Do not substitute XB5AS8442 single NC')
row('SRELAY','24VDC monitored manual reset safety relay',1,'RS India / Pilz India','751103 / PNOZ s3 C 24VDC 2NO','https://in.rsdelivers.com/product/pilz/751103/pilz-pnoz-s3-c-24v-dc-safety-relay-2-safety-1/1919855','India catalogue; quote/stock unconfirmed','Final circuit and achievable diagnostic coverage H09; component does not certify system')
row('SWITCH','Roller lever 1NC+1NO limit/proof switch',9,'Electrihub India','Telemecanique XCKP2118P16','https://electrihub.com/telemecanique-limit-switch-xckp2118p16','Indian listing; stock RFQ','2 directional limits +4 brake proofs +2 prop-pin proofs +1 ballast-restraint proof; mechanical cams and brackets H06; not complete dual-channel safety circuit')
row('GUARDLOCK','Dual-contact positive-opening test-cell gate interlock plus actuator',1,'Schneider/Telemecanique India distributor','XCSB701 + matched XCSZ01 actuator; confirm current pairing','https://electrihub.in/telemecanique-limit-switch-xcsb701','Indian listing; stock and mating key RFQ','Test-cell door, not a patient support lock; placement by cell integrator')
row('POSITION','Absolute 250mm linear potentiometric transducer',1,'Rajvi Instruments / Gefran India channel','Gefran LT-M-0250-P 5kohm','https://rajviinstruments.com/gefran/','India listing; exact drawing/price/stock RFQ','Use3.3V excitation; wiper loading calibration required; full model mounting/end overtravel H06')
row('MCU','Espressif ESP32-S3-DevKitC-1 8MB flash 8MB PSRAM',1,'Mouser India','ESP32-S3-DevKitC-1-N8R8','https://www.mouser.in/en/ProductDetail/Espressif-Systems/ESP32-S3-DevKitC-1-N8R8?qs=sGAEpiMZZMukLrVqQfzRdxL9qjW4vMrDIgqvB9IpdYjh9HGmSaV2DA%3D%3D','Indian regional page listed stock; checkout delivery unconfirmed','N8-only page obsolete/restricted; same DevKitC header, reserve GPIO26..37; PSRAM unused; verify board revision')
row('IMU','GY-521 MPU-6050 fixture IMU',1,'Wavtron','WV-07016','https://www.wavtron.in/products/gy-521-mpu-6050-gyroscope','Low stock1 on listing; not reserved','Verify genuine WHOAMI68 and3.3V I2C pullups; bench supervision only',145,'Listing includes GST')
row('WD','TI external watchdog evaluation module',1,'DigiKey India','TPS3431EVM / 296-50692-ND','https://www.digikey.in/en/products/detail/texas-instruments/TPS3431EVM/9686050','Listing stock2; India checkout/import terms unconfirmed','200ms preset170..230ms; set per TI guide; external latching stop and interface H09',4291.15,'Listed INR; tax freight customs extra/confirm')
row('IO','Isolated OEM command/status and watchdog latching interface assembly',1,'OEM-approved electrical integrator','P0B1-IO; schematic release H02/H09','https://www.linak.in/contact/','CUSTOM RFQ; not released','No invented vendor connector pins; UP/DOWN mutually interlocked contacts, PERMIT dual stop path, 3.3V/field isolation; cannot energize before release')
row('SUPPLY','Certified isolated 24VDC auxiliary DIN supply with protected5V logic branch',1,'Mean Well authorized India distributor','HDR-30-24 plus approved5V isolated branch','https://www.meanwell.com/','India distributor RFQ','Separate from OEM motor supply; charger disconnected during movement; mains by electrician; final load/fuses H09')
row('CONTROL','Enclosure terminal blocks fuses wiring buttons pulldowns and sensor isolation',1,'Electrical integrator','P0B1-HARNESS per final signed schematic','https://www.se.com/in/en/','CUSTOM RFQ; detailed terminal BOM pending H09','3NO spring return22mm UP DOWN RESET; MCP6002-I/P buffer,2x1k,1x1M,1x100ohm,10k ADC bias,2x100nF,1uF per electrical guide; PCB/IO/fuses H09; no direct GPIO coils')
row('EYES','Four forged M10 through-bolt restraint eyes with backing/washers/nuts',4,'Certified industrial lifting accessory supplier India','DIN580 M10; actual load-angle rating required','https://www.crosbygroup.com/','RFQ size origin and angle rating','Restrain ballast only; check4 pan holes11mm and local bearing; do not use for suspension of people')
row('STRAP','Rated polyester ballast restraints with matching shackles',2,'Certified Indian lifting-gear supplier','1t WLL endless web sling; tag and test certificate','https://www.crosbygroup.com/','RFQ exact length and fittings','Wrap closed ballast crate; fixed against translation/tipping; overhead recovery uses independent hoist not these straps')
row('CELL','Independent guarded test cell and interlocked access gate',1,'Industrial guarding integrator','P0B1-CELL 2.5m x2.5m clear internal; height2m minimum','https://www.se.com/in/en/','CUSTOM RFQ; not in apparatus STEP','No access during powered motion; allow external emergency/manual recovery controls; H10; dimensions to site assessment',installed=0)
row('TEST','Calibrated ballast/load cell dial gauge force gauge overhead recovery rig',1,'Test facility','P0B1-TEST','https://www.nabl-india.org/','Facility equipment; verify calibrated ranges','0/5/10/25/50/75kg stages are proposals only; release each by review',installed=0)
row('REVIEW','Mechanical electrical fabrication review machining and inspection services',1,'Qualified mechanical engineer and OEM system integrator','H01..H10 signed release','https://www.linak.in/contact/','RFQ; not a device part','Includes weld calculation NDT independent stop and electrical completion',installed=0)
with (R.parent/'INDIA_BOM_SOURCING.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader();w.writerows(rows)
print(f'{len(rows)} rows; no unknown prices replaced with zero')
