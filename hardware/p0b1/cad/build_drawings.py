#!/usr/bin/env python3
"""Generate a dimensioned A3 review pack from the same manifest as STEP/DXF."""
from pathlib import Path
import json,csv,math,html
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor,white,black
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
R=Path(__file__).resolve().parents[1]
M=json.loads((R/'cad/parts_manifest.json').read_text());P={p['id']:p for p in M['parts']}
C=json.loads((R/'reports/checks.json').read_text())
OUT=R/'drawings/FreeStep_P0B1_review_pack.pdf';OUT.parent.mkdir(exist_ok=True)
W,H=landscape(A3);c=canvas.Canvas(str(OUT),pagesize=(W,H));page=0
INK=HexColor('#193640');TEAL=HexColor('#137c89');GREY=HexColor('#677b81');RED=HexColor('#a33825')
style=ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=16,textColor=INK)
small=ParagraphStyle('small',parent=style,fontSize=9,leading=12)
def para(text,x,y,w,font=11):
 s=style if font==11 else small
 p=Paragraph(text,s);_,h=p.wrap(w,H);p.drawOn(c,x,y-h);return y-h-10
def table(rows,x,y,widths,size=10):
 data=[[Paragraph(html.escape(str(v)).replace('\n','<br/>'),ParagraphStyle('cell',parent=small,fontSize=size,leading=size+3)) for v in row] for row in rows]
 t=Table(data,colWidths=widths,repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#e0eff0')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.35,HexColor('#bbced1')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),3 if size<=8 else 6),('BOTTOMPADDING',(0,0),(-1,-1),3 if size<=8 else 6)]))
 _,h=t.wrap(W,H);t.drawOn(c,x,y-h);return y-h-12
def start(title,sub='Dimensioned engineering review | secured ballast only'):
 global page
 page+=1;c.setFillColor(INK);c.rect(0,H-88,W,88,fill=1,stroke=0)
 c.setFillColor(white);c.setFont('Helvetica-Bold',23);c.drawString(36,H-40,title)
 c.setFont('Helvetica',11);c.drawString(36,H-65,sub)
 c.setFillColor(RED);c.setFont('Helvetica-Bold',10);c.drawString(36,52,'REVIEW ISSUE — NO HUMAN USE — NO FABRICATION OR POWERED-TEST RELEASE')
 c.setStrokeColor(GREY);c.line(36,42,W-36,42);c.setFillColor(INK);c.setFont('Helvetica',9)
 c.drawString(36,27,'FreeStep P0-B1 | 15 Oct 2026 | mm | DO NOT SCALE | authored vendor envelopes')
 c.drawRightString(W-36,27,f'Sheet {page:02d}');c.setFillColor(INK);c.setStrokeColor(INK)
def end():c.showPage()
def view(name,x,y,w,h):
 d=svg2rlg(str(R/'cad/generated/views'/f'{name}.svg'))
 factor=min(w/d.width,h/d.height);d.scale(factor,factor)
 renderPDF.draw(d,c,x,y)
def line(x1,y1,x2,y2):c.line(x1,y1,x2,y2)
def dimh(x1,x2,y,label):
 c.setStrokeColor(TEAL);c.setFillColor(TEAL);c.setLineWidth(.7);line(x1,y,x2,y)
 for x in (x1,x2):line(x-3,y-4,x+3,y+4)
 c.setFont('Helvetica',10);c.drawCentredString((x1+x2)/2,y+7,label);c.setStrokeColor(INK);c.setFillColor(INK)
def dimv(y1,y2,x,label):
 c.saveState();c.translate(x,y1);c.rotate(90);dimh(0,y2-y1,0,label);c.restoreState()

start('FreeStep P0-B1 / build review package')
view('mid',25,110,710,620)
y=H-116
for text in [
 '<b>Purpose:</b> test one guided lift, retained stationary perch and recovery with secured dummy ballast.',
 '<b>Geometry:</b> 250 mm vertical travel; pan top 430 / 555 / 680 mm. Base caster axes 800 x 1000 mm. Steel frame top 1451 mm.',
 f"<b>Mass:</b> nominal custom steel {C['mass']['nominal_custom_steel_kg']:.1f} kg; moving custom steel {C['mass']['moving_custom_steel_kg']:.1f} kg. Purchased parts, welds and guards excluded. Workshop fixture, not portable product.",
 '<b>Selected parts:</b> LINAK LA40PL matched lift kit; HGR25 rail with two HGW25CC blocks; four Blickle 744589 total-lock casters.',
 '<b>Status:</b> supplier fit, structural joints, electrical interfaces, guarding and all physical testing remain open. See H01-H10.',
 '<b>CAD contents:</b> editable solid source, three STEP assembly poses, custom STEP solids, bored plate DXFs, cutlist and manifest. Grey purchased shapes are exclusion envelopes, not OEM CAD.'
]:y=para(text,770,y,370)
end()
start('01 / General arrangement and coordinate datums')
view('front',20,160,530,530);view('side',560,160,570,530)
y=145
y=para('<b>Datums:</b> A = top of four caster plates, Z171. B = guide mounting face, Y140. C = X0 symmetry plane. Floor = Z0; +Y points to ballast. Castor axes X +/-400, Y0/1000.',45,y,1090)
para('<b>Envelope:</b> plates span930 mm X; base legs Y-50..1050; mast top1451. Wheel sweep/pedals and guards can enlarge it. Caster height163 mm provisional; newer catalogue164 mm is H03.',45,y,1090)
end()
start('02 / Travel, guide and actuator interfaces')
for name,x in [('lowered',15),('mid',405),('raised',795)]:
 view(name,x,280,370,440)
 c.setFont('Helvetica-Bold',13);c.drawCentredString(x+185,260,name.upper())
rows=[['Condition','Lowered','Middle','Raised'],['Extension / pan top','0 / 430','125 / 555','250 / 680'],['Actuator upper pin Z','854','979','1104'],['Block centres Z','704 / 1004','829 / 1129','954 / 1254'],['Perch pin row Z','281','406','531']]
table(rows,45,230,[310,255,255,255])
para('LA40PL assumption: lower pin (0,40,330), retracted pin distance524 = stroke250+274, upper pin rises vertically. Clevis gap28.5, PIN12 nominal12. Rail runs Z450..1450. Nominal250mm stroke; usable command travel may be shorter after limit/stop-distance calibration. Verify OEM drawing and all fit tolerances before machining.',45,82,1080,9)
end()
start('03 / Perch props and controlled recovery')
y=H-120
rows=[['Feature','Dimension / function'],['Ladder P08','4 plates, paired wall gap60; PIN16 rows Z281+25n, n0..10; pin axis Y885'],['P15 screw block','50X x70Y x80Z; pin16.5 through X at local Y-15, Z15; M20x2.5 through at Y+15'],['Jackscrew / cap','ISO4017 M20x100-8.8 full thread; exposure17 nominal (14..20); cap40x40x20, underside pocket20.5 x3'],['Moving tab P09','50x85x16; world Y850..935, underside Z380+extension'],['P11 relief','Front edge relief60 wide x6 deep; cap rear edge935, fixed bridge material begins941 in central band'],['Lower-pose height chain','Pin281; P15 bottom266/top346; screw underhead263/tip363; cap360..380; tab underside380']]
y=table(rows,45,y,[260,810])
for text in [
 '<b>Engage:</b> stop at matching25 mm row, release controls, insert and retain both pins, adjust caps toward tabs. Either prop proof inhibits both electrical directions. Use approved OEM manual lowering <=1 mm to seat both.',
 '<b>Release:</b> keep OEM actuator connected and self-locking. Retract screw heads evenly in <=quarter-turn increments, <=3 mm total, until OEM support takes the load and pins are free. Remove only unloaded pins. No bypass of lock input.',
 '<b>Recovery:</b> if pins remain loaded or a screw binds, isolate and use independently rated overhead recovery equipment. Never pry, pull a loaded pin or enter beneath the assembly.',
 '<b>Review:</b> one prop, its tab weld, pin, ladder bridge and screw must be assessed for full moving load. Thread stripping, eccentric bearing, cap friction and fatigue are unverified.'
]:y=para(text,45,y,1070)
end()
# Flat plate detail sheets, each tied to local XY source so rotated assembly holes
# cannot be accidentally specified from a mirrored projection.
for pid in [f'P{n:02d}' for n in range(1,14)]:
 p=P[pid];w,h,t=p['dimensions'];start(f'{pid} / {p["description"].split(";")[0][:72]}')
 s=min(590/w,510/h,3.5);cx=365;cy=390;x=cx-w*s/2;y=cy-h*s/2
 c.setLineWidth(1.2)
 if pid=='P11':
  pts=[(-w/2,-h/2),(-30,-h/2),(-30,-h/2+6),(30,-h/2+6),(30,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2)]
  path=c.beginPath();path.moveTo(cx+pts[0][0]*s,cy+pts[0][1]*s)
  for px,py in pts[1:]:path.lineTo(cx+px*s,cy+py*s)
  path.close();c.drawPath(path)
 else:c.rect(x,y,w*s,h*s)
 for j,hole in enumerate(p['holes'],1):
  hx,hy,d=hole[:3];xx=cx+hx*s;yy=cy+hy*s
  c.circle(xx,yy,d*s/2);c.setFont('Helvetica',8)
  c.drawString(xx+max(5,d*s/2+2),yy+3,str(j))
 c.setStrokeColor(GREY);c.setDash(3,3);line(x-15,cy,x+w*s+15,cy);line(cx,y-15,cx,y+h*s+15);c.setDash();c.setStrokeColor(INK)
 dimh(x,x+w*s,y-34,f'{w:g}');dimv(y,y+h*s,x-30,f'{h:g}')
 c.setFont('Helvetica',10);c.drawString(x,y+h*s+24,'LOCAL XY VIEW: +X right, +Y up; origin = rectangle centre')
 yy=H-122
 for text in [f'<b>Quantity:</b> {p["quantity"]} | <b>Material:</b> {html.escape(p["material"])}',f'<b>Size:</b> {w:g} x {h:g} x {t:g} thick. Thickness extrudes local +Z.',f'<b>Nominal unit mass:</b> {p["unit_mass_kg"]:.3f} kg; sharp-corner/nominal geometry.', '<b>Manufacturing:</b> dimensions in mm. General plate +/-0.3; hole positions +/-0.2 unless tighter vendor requirement. Pair-bore mating plates; deburr. Not a weld release.']:
  yy=para(text,750,yy,380)
 if p['holes']:
  rows=[['#','X','Y','Dia / operation']]
  for j,hole in enumerate(p['holes'],1):
   hx,hy,d,*note=hole
   op='M6 tap pilot5' if d==5 else ('M8 tap pilot6.8' if d==6.8 else ('M12 tap pilot10.2' if d==10.2 else f'{d:g} through'))
   rows.append([j,f'{hx:g}',f'{hy:g}',op])
  yy=table(rows,750,yy,[30,60,70,220],8)
 if pid=='P02':yy=para('Machine datum B after welding. Local +Y becomes world -Z. World stop axes650/1308 correspond local +300/-358. Rail end distance must match received rail.',750,yy,380,9)
 if pid=='P03':yy=para('Mount two HGW25CC blocks at300 mm centres. Each57 x45 M8 pattern. Machine mating face after welding. Confirm OEM torque/thread depth.',750,yy,380,9)
 if pid in ('P05','P06'):yy=para('Final bore/ear spacing subject to current OEM eye drawing. Pair-bore ears after welding; no forced pin alignment.',750,yy,380,9)
 if pid=='P11':yy=para('MANDATORY centred front-edge relief:60 wide x6 deep through thickness12. Front is local -Y. Do not fill notch with weld.',750,yy,380)
 if pid=='P07':yy=para('Ballast pan only. Four M10 through-bolt restraint eyes with reviewed backing/washers/nuts. No human seat or sling attachment rating.',750,yy,380)
 para('DXF: cad/generated/dxf/'+pid+'.dxf | STEP: cad/generated/parts/'+pid+'.step',45,90,1050,9)
 end()
start('P15 / Prop screw block machining')
# Top XY and side YZ, explicit coordinates.
x,y,s=90,275,3.8
c.rect(x,y,70*s,80*s);c.circle(x+20*s,y+15*s,16.5*s/2)
c.setDash(4,3);line(x+50*s,y,x+50*s,y+80*s);c.setDash()
dimh(x,x+70*s,y-28,'70 along Y');dimv(y,y+80*s,x-28,'80 along Z')
c.setFont('Helvetica-Bold',12);c.drawString(x,y+80*s+24,'SIDE YZ (pin hole axis X)')
c.setFont('Helvetica',10);c.drawString(x,y-60,'Circle centre: Y-15 from part centre, Z15 from underside')
x2,y2=530,340;c.rect(x2,y2,50*s,70*s);c.circle(x2+25*s,y2+50*s,17.5*s/2)
dimh(x2,x2+50*s,y2-28,'50 along X');dimv(y2,y2+70*s,x2-28,'70 along Y')
c.setFont('Helvetica-Bold',12);c.drawString(x2,y2+70*s+24,'TOP XY (thread axis Z)')
yy=H-130
for txt in ['<b>Qty2; certified S355.</b> Local XY origin at rectangle centre; bottomZ0.', '<b>Thread:</b> drill17.5 then tap M20x2.5-6H THROUGH80. Gauge both ends. Do not assemble bolt into an untapped CAD pilot.', '<b>Pin:</b> bore16.5 through X at localY-15/Z15. Axis separation30 from thread; nominal ligament11.75. No sharp internal burrs.', '<b>Mate:</b> full-thread ISO4017 M20x100-8.8, entered from below. Screw head remains accessible. Apply engineer-approved thread lubricant; record condition.', '<b>Hold:</b> full-load thread/pin bearing and eccentric compression review H07. No safety factor or certified capacity assigned.']:
 yy=para(txt,820,yy,310)
end()
start('P16 / Prop cap and P17 / Rail retention stop')
yy=H-125
yy=table([['Part','Qty / blank','Machining and assembly'],['P16','2 /40x40x20','Underside pocket diameter20.5 x3 deep, centred. No through hole or thread. Top face contacts P09; slack non-load-bearing tether.'],['P17','4 /16X x36Y x20Z','Through bore8.5 parallel Y at X0/Z10; local origin XY centre, bottomZ0. Two at each rail-end working limit.'],['P17 installation','M8x55 tentative','Backing P02 tap M8-6H at world X+/-26 and Z650/1308. Stop bodies bottomZ640/1298, Y140..176. Nominal2mm gap to blocks at operational ends.']],45,yy,[110,230,730])
x,y,s=120,200,5
c.rect(x,y,40*s,40*s);c.circle(x+20*s,y+20*s,20.5*s/2);dimh(x,x+40*s,y-28,'40');dimv(y,y+40*s,x-28,'40')
c.setFont('Helvetica-Bold',12);c.drawString(x,y+40*s+26,'P16 UNDERSIDE; pocket depth3')
x,y=610,200;c.rect(x,y,16*s,20*s);c.circle(x+8*s,y+10*s,8.5*s/2);dimh(x,x+16*s,y-28,'16');dimv(y,y+20*s,x-28,'20')
c.setFont('Helvetica-Bold',12);c.drawString(x,y+20*s+26,'P17 XZ; bore through Y36')
para('Retention stops limit guide overtravel; they are not qualified fall-arrest devices. Locate hardwired limits to stop before contact. Their bolt/thread/backing/dynamic strength is H08. Screw length includes actual washer,36mm stop and16mm backing engagement; verify no bottoming.',45,110,1060)
end()
start('Pins / Material, bores and positive retention')
for pid,y in [('PIN12',480),('PIN16',230)]:
 p=P[pid];d=p['diameter'];L=p['cut_length'];s=6
 c.rect(90,y,L*s,d*s)
 for z in (5,L-5):
  xx=90+z*s;line(xx,y,xx,y+d*s);c.setDash(3,3);line(xx,y-6,xx,y+d*s+6);c.setDash()
 dimh(90,90+L*s,y-30,str(L));dimv(y,y+d*s,65,f'D{d}')
 c.setFont('Helvetica-Bold',15);c.drawString(90,y+d*s+36,pid+' / qty'+str(p['quantity']))
 para('EN8/C45 certified. Cross drill diameter3 at5 from EACH end, through diameter. Deburr bores. Retain BOTH ends using new3x25 split pins and flat washers. Nominal clearance mating bore12.5 or16.5; engineer approve fit. Pins are not threaded bolts.',820,y+d*s+30,300)
end()
start('Stock / Tube cutlist and first-fit nesting')
rows=[['ID','Qty','RHS outside / wall','Length','Description']]
for p in P.values():
 if 'section' in p:rows.append([p['id'],p['quantity'],' x '.join(map(str,p['section'])),p['cut_length'],p['description']])
y=table(rows,45,H-120,[75,55,180,85,675])
y=para('All cuts square at both ends. Same80x40 section may rotate in assembly. First-fit plan uses6000mm bars,20mm trim EACH end and3mm kerf per cut; real supplier length/kerf may differ.',45,y,1060)
for b in C['stock_nest']:
 y=para('<b>Bar '+str(b['section_mm'])+' #'+str(b['bar'])+':</b> '+', '.join(f'{p}:{l}' for p,l in b['parts'])+f" | usable offcut {b['offcut_mm']} mm",45,y,1060)
end()
start('Review / Screening calculations and limitations')
S=C['screening'];rows=[['Screen','Result / assumption'],['Payload study','75kg added ballast; not a working-load rating'],['Moving gravity force',f"{S['moving_gravity_N']:.0f}N including nominal moving steel, excluding vendor moving mass"],['Arm beam bending',f"{S['arm_simple_bending_MPa']:.1f}MPa gravity; {S['arm_8000N_blocked_drive_MPa']:.1f}MPa at8000N blocked-drive screen;660mm arm, equal sharing"],['Guide couple per block',f"{S['guide_couple_per_block_N']:.0f}N gravity; {S['guide_8000N_fault_couple_per_block_N']:.0f}N fault;300mm spacing, compare C0=52820N with combined loads"],['Pins nominal double shear',f"PIN12 {S['pin12_8000N_double_shear_MPa']:.1f}MPa; PIN16 {S['pin16_8000N_double_shear_MPa']:.1f}MPa,8000N each; local bearing omitted"],['Caster screen',f"Steel+75kg /3 = {S['three_caster_average_load_kg']:.1f}kg per caster; catalogue110kg each; actual unequal distribution and supplier service factors pending"]]
y=table(rows,45,H-120,[270,800])
for text in C['limitations']:y=para('- '+html.escape(text),45,y,1070)
para('Passing geometric assertions is not a structural pass. Use reports/checks.json and tests/check_design.py to reproduce values. No physical measurements or tests were performed.',45,90,1060)
end()
start('Release / Assembly, procurement and bench gates')
rows=[['Hold','Evidence required before proceeding'],['H01-H04','Current OEM lift code/interfaces; caster revision; genuine matched guide set and machining requirements'],['H05-H08','Certified material, full structural/weld/joint review, sensor and proof brackets, one-prop retention and independent stop engineering'],['H09-H10','Final terminal schematic/IO/harness and independent stop tests; guarded cell, calibrated instruments, recovery rig and staged release']]
y=table(rows,45,H-120,[170,900])
for txt in [
 '<b>Assembly:</b> fixed weldment -> finish-machine guide face -> moving frame -> guided dry sweep -> qualified endstops -> OEM actuator/pins -> props -> ballast restraints/sensors -> guarded cell -> signed electrical integration. Full joint schedule W01-W17 in ASSEMBLY_PLAN.md.',
 '<b>India procurement:</b>60 rows in INDIA_BOM_SOURCING.csv. Four dated-price lines total INR16413.15 with mixed tax bases; this is an incomplete subtotal. OEM kit, fabrication, guarding, integration and test facility are unquoted. Stock listings are not reservations.',
 '<b>Physical stages:</b> lamps and fault injection first; then no added ballast; then proposed5/10/25/50/75kg only after reviewer release. Test stop travel, sensor faults, perch dwell, power loss, emergency recovery and floor stability. No physical cases have passed.',
 '<b>Not included as released detail:</b> human seat/support, approved electrical connector pins, IO PCB, cable routing, final guard cell, match-drilled sensor/cam brackets, joint torques or weld throat sizing. These are explicit holds, not optional fabrication choices.',
 '<b>Source documents:</b> README.md, ASSEMBLY_PLAN.md, ELECTRICAL_INTEGRATION.md, BENCH_TEST_PLAN.md, RELEASE_HOLDS.csv, procurement/INDIA_SELECTION.md and reports/checks.json accompany this PDF.'
]:y=para(txt,45,y,1070)
end();c.save();print(f'{OUT}: {page} A3 sheets')
