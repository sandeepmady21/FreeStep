#!/usr/bin/env python3
"""Round-trip committed STEP solids and plate DXFs; independent of model generation."""
from pathlib import Path
import json
import cadquery as cq
R=Path(__file__).resolve().parents[1]
m=json.loads((R/'cad/parts_manifest.json').read_text());n=0
for p in m['parts']:
 if p['kind']!='custom':continue
 path=R/'cad/generated/parts'/(p['id']+'.step');s=cq.importers.importStep(str(path)).val()
 assert s.isValid(),path
 assert abs(s.Volume()-p['volume_mm3'])<=max(0.01,p['volume_mm3']*1e-6),path
 n+=1
 dxf=R/'cad/generated/dxf'/(p['id']+'.dxf')
 if dxf.exists():
  shape=cq.importers.importDXF(str(dxf)).wires().toPending().extrude(p['dimensions'][2]).val()
  assert shape.isValid(),dxf
  assert abs(shape.Volume()-p['volume_mm3'])<=max(0.01,p['volume_mm3']*1e-6),dxf
  n+=1
for path in (R/'cad/generated/assemblies').glob('*.step'):
 s=cq.importers.importStep(str(path)).val();assert s.isValid() and s.Volume()>0,path;n+=1
assert n==44,n
print(f'{n} STEP/DXF round-trip checks passed; not physical/structural approval')
