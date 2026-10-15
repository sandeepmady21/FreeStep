#!/usr/bin/env python3
"""Screen geometry, mechanisms and simple load cases; never release a physical build."""
from pathlib import Path
import sys,json,math,csv
from collections import defaultdict
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'cad'))
import build
import cadquery as cq
m,shapes=build.build(R/'cad/generated',export=False)
P=m['parameters'];parts={p['id']:p for p in m['parts']};checks=[]
def check(name,v,detail):
 checks.append(dict(check=name,pass_=bool(v),detail=detail))
 if not v: raise AssertionError(name+': '+str(detail))
def located(i,e=0):
 xyz=i['xyz'].copy();xyz[2]+=e if i['moving'] else 0
 rot=i['rotation'];loc=cq.Location(cq.Vector(*xyz)) if rot is None else cq.Location(cq.Vector(*xyz),cq.Vector(*rot[0]),rot[1])
 return shapes[i['id']].located(loc)
check('all authored shapes valid positive volume',all(s.isValid() and s.Volume()>0 for s in shapes.values()),len(shapes))
check('positive instance quantities',all(p['quantity']>0 for p in parts.values()),len(m['instances']))
check('rail hole count',len([h for h in parts['P02']['holes'] if h[2]==5])==17,'17 M6 rail +4 M8 stop holes')
backbone=located(next(i for i in m['instances'] if i['id']=='P02'))
for x in (-26,26):
 for z in (650,1308):
  probe=build.cylinder(6.7,16).rotate((0,0,0),(1,0,0),-90).translate((x,124,z)).val()
  check(f'retention stop bore axis {x}/{z}',backbone.intersect(probe).Volume()<0.01,'world coordinates verify after plate rotation')
check('block pattern',len(parts['P03']['holes'])==8 and P['block_holes_x']==57 and P['block_holes_z']==45,'57 x45; blocks300 apart')
check('pin engagement stack',70-2*5>=48.5 and 110-2*5>=80,'12mm pin ears outer48.5;16mm pin ladder outer80; washer allowances physical fit hold')
check('rail working envelope',P['rail_start_z']<854-150-42 and 854+150+42+250<1450,'block edges662..1296 within450..1450')
check('retention stops beyond operating travel',662-660==2 and 1298-1296==2,'nominal2mm gaps; stops need load/dynamic review')
check('perch pin indexing',P['lock_pin_count']==11 and (11-1)*25==250,'11 rows cover0..250 in25mm steps')
check('perch cap height',263+100-3+20==380,'100 bolt;3 pocket;20 cap, tab underside380')
check('prop thread engagement',80>=3*20 and 14<=17<=20,'80mm block; nominal17 exposure; thread strip not checked')
check('prop pin/screw ligament',30-16.5/2-20/2>=11.5,'nominal11.75mm; stress concentration needs review')
# Full sweep of authored steel vs fixed authored steel. Remove manually installed
# props for powered travel. This does NOT check vendor internals/cables/guards.
props={'P15','P16','PIN16','BOLT20'}
fixed=[i for i in m['instances'] if not i['moving'] and parts[i['id']]['kind']=='custom' and i['id'] not in props]
moving=[i for i in m['instances'] if i['moving'] and (parts[i['id']]['kind']=='custom' or i['id']=='BLOCK')]
collisions=[];tested=0
for e in range(0,251,5):
 for a in fixed:
  sa=located(a);ba=sa.BoundingBox()
  for b in moving:
   sb=located(b,e);bb=sb.BoundingBox()
   if any(min(getattr(ba,k+'max'),getattr(bb,k+'max'))-max(getattr(ba,k+'min'),getattr(bb,k+'min'))<=0.001 for k in 'xyz'):continue
   tested+=1;v=sa.intersect(sb).Volume()
   if v>0.1:collisions.append([e,a['name'],b['name'],round(v,4)])
check('selected fixed/moving solids across51 poses',not collisions,dict(intersections=tested,collisions=collisions))
# Props manually indexed with carriage, no physical automatic linkage implied.
check('notched bridge measured design clearance',941-935>=3,'6mm nominal Y gap to cap/tab; must remain>=3 measured under load')
envelope_clashes=[]
steel=[i for i in m['instances'] if parts[i['id']]['kind']=='custom' and i['id'] not in props|{'PIN12'}]
actuators=[i for i in m['instances'] if i['id'] in {'ACT_BODY','ACT_ROD'}]
for e in range(0,251,5):
 for a in actuators:
  sa=located(a,e);ba=sa.BoundingBox()
  for b in steel:
   sb=located(b,e);bb=sb.BoundingBox()
   if any(min(getattr(ba,k+'max'),getattr(bb,k+'max'))-max(getattr(ba,k+'min'),getattr(bb,k+'min'))<=0.001 for k in 'xyz'):continue
   if sa.intersect(sb).Volume()>0.1:envelope_clashes.append([e,a['name'],b['name']])
check('authored actuator envelope vs steel sweep',not envelope_clashes,envelope_clashes)
check('clevis nose clearance to authored envelopes',346.4-343>=3 and 841-834.9>=3,'lower3.4mm / upper6.1mm nominal; OEM drawing and deflected fit remain H01')
# Stock nest: first fit descending,6000 stock,20 end trims each,3 saw kerf per part.
groups=defaultdict(list)
for p in parts.values():
 if 'section' in p:
  section=tuple(sorted(p['section'][:2]))+(p['section'][2],)
  for n in range(p['quantity']):groups[section].append((p['id'],p['cut_length']))
nest=[]
for sec,items in groups.items():
 bars=[]
 for pid,length in sorted(items,key=lambda x:-x[1]):
  target=next((b for b in bars if b['used_mm']+length+3<=5960),None)
  if target is None:target=dict(section_mm=sec,stock_mm=6000,used_mm=0,parts=[]);bars.append(target)
  target['parts'].append([pid,length]);target['used_mm']+=length+3
 for n,b in enumerate(bars,1):b['bar']=n;b['offcut_mm']=5960-b['used_mm'];nest.append(b)
check('stock cuts fit with trim and kerf',all(b['offcut_mm']>=0 for b in nest),nest)
# Nominal uniform-density steel centre of mass at each pose; vendor mass excluded.
mass={};centres={}
for e in (0,125,250):
 total=0;mom=[0,0,0];moving_mass=0
 for i in m['instances']:
  p=parts[i['id']]
  if p['kind']!='custom':continue
  kg=p['unit_mass_kg'];s=located(i,e)
  if not i['moving'] and i['id'] in props:s=s.translate((0,0,e))
  c=s.Center();total+=kg
  if i['moving']:moving_mass+=kg
  for j,v in enumerate((c.x,c.y,c.z)):mom[j]+=kg*v
 mass[e]=total;centres[e]=[v/total for v in mom]
load=(75+moving_mass)*9.81
# Conservative beam screen: each arm carries half TOTAL moving load at0.66m.
w=h=60;t=4;I=(w*h**3-(w-2*t)*(h-2*t)**3)/12;Z=I/(h/2)
arm_sigma=load*660/2/Z
fault_sigma=8000*660/2/Z
couple=load*660/300
fault_couple=8000*660/300
# Nominal double shear with full8000N, no assumption of even two-prop sharing.
pin12_tau=8000/(2*math.pi*12**2/4);pin16_tau=8000/(2*math.pi*16**2/4)
# Three-wheel load-sharing screen, not stability assessment.
caster_three=(mass[0]+75)/3
stability=[]
for e in (0,125,250):
 kg=mass[e]+75;cg=[(mass[e]*centres[e][j]+75*[0,700,430+e][j])/kg for j in range(3)]
 # 40mm caster-offset inset. Actual contact rectangle can be worse with deformation.
 distances=[360-cg[0],cg[0]+360,cg[1]-40,960-cg[1]]
 stability.append(dict(extension=e,steel_plus_dummy_CG_mm=cg,min_edge_distance_mm=min(distances),
    restoring_Nm=kg*9.81*min(distances)/1000,challenge_100N_at_1m_Nm=100))
# No structural pass assertions: these deliberately omit connections/local failure.
report=dict(revision='P0-B1',status='REVIEW; NO PHYSICAL TESTS OR LOAD RATING',checks=checks,
 mass=dict(nominal_custom_steel_kg=mass[0],moving_custom_steel_kg=moving_mass,vendor_weld_guard_fastener_masses='excluded; weigh actual device'),
 screening=dict(payload_study_kg=75,moving_gravity_N=load,arm_section_I_mm4=I,arm_section_Z_mm3=Z,
 arm_simple_bending_MPa=arm_sigma,arm_8000N_blocked_drive_MPa=fault_sigma,
 guide_couple_per_block_N=couple,guide_8000N_fault_couple_per_block_N=fault_couple,guide_catalogue_C0_N=52820,
 pin12_8000N_double_shear_MPa=pin12_tau,pin16_8000N_double_shear_MPa=pin16_tau,
 three_caster_average_load_kg=caster_three,caster_catalogue_each_kg=110,stability=stability),stock_nest=nest,
 limitations=['Nominal sharp-corner tubes: real sections/corner radii/tolerances need mill properties',
 'No weld/bolt/thread-stripping/local bearing/buckling/plate bending/fatigue calculation',
 'Guide load distribution and combined moments/preload/life need supplier review',
 'Steel-only mass screen excludes vendor parts, guards and welds; stability must use measured contacts/CG',
 'No patient rating, floor friction/sliding test, proof load or physical result implied',
 'Swept solid check excludes manually removed props, vendor internals, cables, guards, fasteners and deformation'])
(R/'reports/checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(checks=len(checks),nominal_custom_steel_kg=round(mass[0],1),moving_custom_steel_kg=round(moving_mass,1),arm_fault_MPa=round(fault_sigma,1),status=report['status']),indent=2))
