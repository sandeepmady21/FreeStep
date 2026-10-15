#!/usr/bin/env python3
"""Editable solid CAD for P0-B1. Vendor parts are explicit fit envelopes.

Generates real hollow tubes, bored plates, STEP assemblies and DXF sections.
The manufacturing issue remains REVIEW until the supplier/interface holds close.
This program is not a structural certification or a collision-free design claim.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import xml.etree.ElementTree as ET
import cadquery as cq
from OCP.gp import gp_Ax2, gp_Pnt, gp_Dir

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
P = json.loads((ROOT / "parameters.json").read_text())
STEEL = cq.Color(0.32, 0.39, 0.44)
MOVING = cq.Color(0.12, 0.43, 0.50)
VENDOR = cq.Color(0.73, 0.76, 0.77)
LOCK = cq.Color(0.95, 0.62, 0.15)


def orient_svg(path, projection):
    """OCC chooses its own camera roll. Orient world Z up (+Y up in plan)."""
    path=Path(path);root=ET.fromstring(path.read_text())
    if root.get("data-z-up"): return
    axis=gp_Ax2(gp_Pnt(),gp_Dir(*projection))
    x,y=axis.XDirection().Z(),axis.YDirection().Z()
    if math.hypot(x,y)<1e-8:
        x,y=axis.XDirection().Y(),axis.YDirection().Y()
    angle=-90-math.degrees(math.atan2(-y,x))
    w,h=float(root.get("width")),float(root.get("height"))
    rad=math.radians(angle);nw=abs(w*math.cos(rad))+abs(h*math.sin(rad));nh=abs(w*math.sin(rad))+abs(h*math.cos(rad))
    ns="http://www.w3.org/2000/svg";ET.register_namespace("",ns)
    group=ET.Element("{"+ns+"}g",transform=f"translate({nw/2},{nh/2}) rotate({angle}) translate({-w/2},{-h/2})")
    for child in list(root):root.remove(child);group.append(child)
    root.append(group);root.set("width",str(nw));root.set("height",str(nh));root.set("viewBox",f"0 0 {nw} {nh}");root.set("data-z-up","true")
    path.write_text(ET.tostring(root,encoding="unicode"))


def plate(w, h, t, holes=()):
    body = cq.Workplane("XY").rect(w, h).extrude(t)
    for x, y, diameter, *_ in holes:
        cutter = cq.Workplane("XY").center(x, y).circle(diameter / 2).extrude(t)
        body = body.cut(cutter)
    return body


def tube(w, h, t, length):
    return cq.Workplane("XY").rect(w, h).rect(w-2*t, h-2*t).extrude(length)


def cylinder(d, length):
    return cq.Workplane("XY").circle(d/2).extrude(length)


def build(out, export=True):
    out = Path(out)
    for d in ("parts", "dxf", "assemblies", "views"):
        (out / d).mkdir(parents=True, exist_ok=True)
    definitions, instances, shapes = {}, [], {}

    def define(pid, shape, description, kind="custom", material="S355 / YSt355; mill certificate required", **extra):
        shape = shape.val() if isinstance(shape, cq.Workplane) else shape
        if not shape.isValid() or shape.Volume() <= 0:
            raise ValueError(f"Invalid/empty solid {pid}")
        definitions[pid] = dict(id=pid, description=description, kind=kind,
                               material=material, volume_mm3=shape.Volume(), **extra)
        shapes[pid] = shape

    def inst(pid, name, xyz, rotation=None, moving=False, color=None):
        # Rotation is axis vector and degrees, applied in local origin first.
        loc = cq.Location(cq.Vector(*xyz)) if rotation is None else cq.Location(
            cq.Vector(*xyz), cq.Vector(*rotation[0]), rotation[1])
        instances.append(dict(id=pid, name=name, xyz=list(xyz), rotation=rotation,
                              moving=moving, color=color or (MOVING if moving else STEEL)))
        return loc

    caster_holes = [(x,y,9,"through M8 clearance") for x in (-37.5,37.5) for y in (-22.5,22.5)]
    rail_holes = [(0,-480+60*n,5,"M6-6H through; drill 5 then tap; verify rail end distance") for n in range(17)]
    # P02 local Y maps to world -Z: local +300/-358 -> world650/1308.
    rail_holes += [(x,z,6.8,"M8-6H through for independent retention stop") for x in (-26,26) for z in (300,-358)]
    block_holes = [(x,z,8.5,"through M8 clearance") for x in (-28.5,28.5)
                   for z in (-172.5,-127.5,127.5,172.5)]
    ladder_holes = [(-15,-144+25*n,16.5,"through; ream paired plates together") for n in range(11)]
    plate_defs = [
        ("P01",130,110,8,caster_holes,"Caster plate; use 75 x 45 mounting option"),
        ("P02",200,1000,16,rail_holes,"Mast backing plate; machine guide face after welding"),
        ("P03",220,420,12,block_holes,"Moving bridge; mounting face machined after welding"),
        ("P04",100,100,12,[(x,y,13,"M12 clearance") for x in (-35,35) for y in (-35,35)],"Lower clevis removable base"),
        ("P05",70,60,10,[(0,17,12.5,"actuator pin clearance; final match OEM eye")],"Lower clevis ear; short nose clears motor"),
        ("P06",70,43,10,[(0,-8.5,12.5,"actuator pin clearance; final match OEM eye")],"Upper clevis ear; short nose clears MLF housing"),
        ("P07",400,320,6,[(x,y,11,"M10 ballast restraint") for x in (-160,160) for y in (-110,110)],"Ballast pan; not a patient seat"),
        ("P08",70,350,10,ladder_holes,"Perch prop ladder plate; horizontal local = world Y"),
        ("P09",50,85,16,[],"Moving prop contact tab; rear edge Y935 clears relieved bridges"),
        ("P10",120,180,20,[(x,y,10.2,"M12-6H through after welding") for x in (-35,35) for y in (-55,15)],"Lower clevis pedestal landing"),
        ("P11",80,35,12,[],"Ladder-to-post bridge"),
        ("P12",50,30,30,[],"Moving yoke spacer to bridge"),
        ("P13",100,100,6,[],"Square mast/base web; weld per assembly map"),
    ]
    for pid,w,h,t,holes,desc in plate_defs:
        solid=plate(w,h,t,holes)
        if pid=="P11":
            solid=solid.cut(cq.Workplane("XY").center(0,-14.5).rect(60,6).extrude(t))
            desc += "; 60 wide x 6 deep front-edge relief, centred, through thickness"
        define(pid,solid,desc,dimensions=[w,h,t],holes=holes)
    # The prop screw thread is specified on the drawing; root cylinder is not a
    # substitute for the M20-6H tapping operation.
    lock_block = cq.Workplane("XY").box(50,70,80,centered=(True,True,False))
    lock_block = lock_block.cut(cylinder(17.5,80).translate((0,15,0)))
    lock_block = lock_block.cut(cylinder(16.5,60).rotate((0,0,0),(0,1,0),90).translate((-30,-15,15)))
    define("P15",lock_block,"Perch screw block; M20-6H through at local Y+15; cross pin at Y-15 Z15",
           dimensions=[50,70,80],operations="Tap M20x2.5 through; bore cross pin 16.5 through X; verify 11.75 mm nominal ligament")
    cap=cq.Workplane("XY").box(40,40,20,centered=(True,True,False)).cut(cylinder(20.5,3))
    define("P16",cap,"Perch cap; underside 20.5 dia x 3 deep locates screw tip; tether outside load path",
           dimensions=[40,40,20],operations="Circular pocket from underside; no thread; grease contact")
    stop=cq.Workplane("XY").box(16,36,20,centered=(True,True,False))
    stop=stop.cut(cylinder(8.5,36).rotate((0,0,0),(1,0,0),-90).translate((0,-18,10)))
    define("P17",stop,"Independent carriage retention stop; 8.5 cross bore through Y at Z10",
           dimensions=[16,36,20],operations="Cross drill 8.5 through Y; bolt M8x55 tentative; dynamic capacity requires review")
    # Separate stock IDs prevent quantity/length ambiguity in the cutlist.
    stock = [
        ("T01",40,80,4,1100,"Base longitudinal leg"),
        ("T02",80,40,4,760,"Front base cross member"),
        ("T03",80,40,4,1200,"Mast post"),
        ("T04",60,60,4,580,"Moving front cross member"),
        ("T10",60,60,4,460,"Moving middle cross member; fits between continuous side arms"),
        ("T05",60,60,4,790,"Moving side arm; square-cut butt joints"),
        ("T06",60,60,4,460,"Ballast support drop"),
        ("T07",60,60,4,700,"Ballast cross member"),
        ("T08",60,60,4,500,"Stationary prop support post"),
        ("T09",60,60,4,100,"Prop-post base outrigger"),
    ]
    for pid,w,h,t,length,desc in stock:
        define(pid,tube(w,h,t,length),desc,section=[w,h,t],cut_length=length)
    # Pins include real cross-holes for split pins; do not use threaded bolts as pins.
    for pid,dia,length in [("PIN12",12,70),("PIN16",16,110)]:
        pin=cylinder(dia,length)
        for z in (5,length-5):
            pin=pin.cut(cylinder(3,diameter_span:=dia+2).rotate((0,0,0),(0,1,0),90).translate((-diameter_span/2,0,z)))
        define(pid,pin,"Turned EN8/C45 clevis pin; 3 mm split-pin holes at 5 from each end",
               material="EN8/C45 with material certificate",diameter=dia,cut_length=length)
    define("BOLT20",cylinder(20,100).union(cq.Workplane("XY").polygon(6,34.641).extrude(13).translate((0,0,-13))),
           "ISO 4017 M20x100-8.8 full thread; schematic thread envelope",kind="purchased",material="8.8 fastener")

    # Fixed steel assembly. Base top = 163+8+80=251.
    base_top = P["caster_height"] + 8 + 80
    for side in (-1,1):
        x=side*400
        for yy in (0,1000): inst("P01",f"caster_plate_{side}_{yy}",(x,yy,163))
        inst("T01",f"base_leg_{side}",(x,-50,211),((1,0,0),-90))
        inst("T03",f"mast_post_{side}",(side*70,104,base_top))
        inst("T08",f"prop_post_{side}",(side*330,1000,base_top))
        inst("T09",f"prop_outrigger_{side}",(280 if side==1 else -380,1000,221),((0,1,0),90))
        inst("P13",f"mast_web_{side}",(110 if side==1 else -116,150,301),((1,1,1),120))
        for xx in (side*330-35,side*330+35):
            # Local plate XY -> global YZ, extrusion -> global X.
            inst("P08",f"ladder_{side}_{xx}",(xx-5,900,425),((1,1,1),120),color=LOCK)
        for zz in (275,575): inst("P11",f"ladder_bridge_{side}_{zz}",(side*330,952.5,zz))
    inst("T02","base_front_cross",(-380,100,211),((0,1,0),90))
    # Plate local XY -> global XZ; thickness toward +Y after -90 about X.
    inst("P02","machined_backbone",(0,124,950),((1,0,0),-90))
    for x in (-26,26):
        for z in (640,1298): inst("P17",f"rail_retention_stop_{x}_{z}",(x,158,z),color=LOCK)
    inst("P10","lower_pedestal",(0,60,base_top))
    inst("P04","lower_clevis_base",(0,40,base_top+20))
    for side in (-1,1):
        inst("P05",f"lower_clevis_ear_{side}",(side*19.25-5,40,313),((1,1,1),120))
    inst("PIN12","lower_actuator_pin",(-35,40,330),((0,1,0),90),color=LOCK)

    # Purchased parts: interface envelopes, not redistributed vendor CAD.
    rail=cq.Workplane("XY").box(23,22,1000,centered=(True,False,False))
    for n in range(17):
        cutter=cylinder(7,25).rotate((0,0,0),(1,0,0),-90).translate((0,-1,20+n*60))
        rail=rail.cut(cutter)
    define("RAIL",rail,"HIWIN HGR25R1000; nominal rail mount envelope; verify 20 mm end distance",kind="purchased",material="Vendor alloy steel")
    # Block housing excludes the rail's occupied region; model is a collision envelope.
    block=cq.Workplane("XY").box(70,30.5,84,centered=(True,False,True)).translate((0,5.5,0))
    block=block.cut(cq.Workplane("XY").box(23.2,22.1,86,centered=(True,False,True)))
    define("BLOCK",block,"HIWIN HGW25CC; H36 W70 L84; 57x45 M8 pattern",kind="purchased",material="Vendor alloy steel")
    inst("RAIL","HGR25_rail",(0,140,450),color=VENDOR)
    caster=cq.Workplane("XY").box(90,66,6,centered=(True,True,False)).translate((0,0,157))
    caster=caster.union(cylinder(125,32).rotate((0,0,0),(0,1,0),90).translate((-16,40,62.5)))
    caster=caster.union(cq.Workplane("XY").box(45,55,55).translate((0,20,130)))
    define("CASTER",caster,"Blickle LWK-TPA126G-FI-P25; own envelope only; pedal/sweep need physical check",kind="purchased",material="Vendor polymer/steel")
    for x in (-400,400):
        for y in (0,1000): inst("CASTER",f"caster_{x}_{y}",(x,y,0),color=VENDOR)
    # 0404022 reference envelope: housing starts16.4 above lower pin;
    # transverse165.5, asymmetry conservatively enclosed by122mm width.
    motor=cylinder(46,350).translate((0,0,30)).union(cq.Workplane("XY").box(122,165.5,109).translate((0,-49.25,70.9)))
    define("ACT_BODY",motor,"LINAK LA40 PL manual-lowering own exclusion envelope; not vendor model",kind="purchased",material="OEM assembly")
    rod=cylinder(28,394).union(cylinder(46,79.9).translate((0,0,295)))
    define("ACT_ROD",rod,"LA40 PL telescoping rod and MLF envelope; nominal housing ends19.1 below upper pin; supplier hold",kind="purchased",material="OEM assembly")
    inst("ACT_BODY","LA40_PL_body",(0,40,330),color=VENDOR)
    define("CTRL",cq.Workplane("XY").box(180,120,300),"Reserved CBJ2/BAJ enclosure volume; final brackets match-drilled",kind="purchased",material="OEM assembly")
    inst("CTRL","OEM_control_reservation",(0,-100,1000),color=VENDOR)

    # Moving assembly, coordinates at fully retracted actuator (pin Z854).
    centre = P["actuator_bottom_pin_z"] + P["actuator_retracted_pin_distance"]
    yoke_z = centre + 60
    inst("P03","moving_bridge",(0,176,centre),((1,0,0),-90),moving=True)
    for dz in (-150,150): inst("BLOCK",f"HGW25_block_{dz}",(0,140,centre+dz),moving=True,color=VENDOR)
    inst("T04","moving_front_cross",(-290,40,yoke_z),((0,1,0),90),moving=True)
    inst("T10","moving_middle_cross",(-230,248,yoke_z),((0,1,0),90),moving=True)
    # Side arms butt against end crossmember. Nominal source length is fixed in the cutlist.
    for side in (-1,1):
        inst("T05",f"moving_arm_{side}",(side*260,70,yoke_z),((1,0,0),-90),moving=True)
        for yy in (580,820):
            inst("T06",f"seat_drop_{side}_{yy}",(side*260,yy,424),moving=True)
        inst("P12",f"bridge_spacer_{side}",(side*80,203,centre+60),moving=True)
        inst("P06",f"upper_clevis_ear_{side}",(side*19.25-5,40,centre+8.5),((1,1,1),120),moving=True)
        inst("P09",f"prop_contact_{side}",(side*330,892.5,380),moving=True,color=LOCK)
    for yy in (580,820): inst("T07",f"seat_cross_{yy}",(-350,yy,394),((0,1,0),90),moving=True)
    inst("P07","secured_ballast_pan",(0,700,424),moving=True)
    inst("PIN12","upper_actuator_pin",(-35,40,centre),((0,1,0),90),moving=True,color=LOCK)
    inst("ACT_ROD","LA40_PL_rod",(0,40,centre-394),moving=True,color=VENDOR)

    # Props are manually indexed, not mechanically coupled to the carriage.
    for side in (-1,1):
        inst("P15",f"prop_screw_block_{side}",(side*330,900,281-15),color=LOCK)
        inst("PIN16",f"prop_pin_{side}",(side*330-55,885,281),((0,1,0),90),color=LOCK)
        inst("BOLT20",f"prop_jackscrew_{side}",(side*330,915,263),color=LOCK)
        inst("P16",f"prop_cap_{side}",(side*330,915,360),color=LOCK)

    report = []
    for pose,extension in (("lowered",0),("mid",125),("raised",250)):
        assy=cq.Assembly(name=f"FreeStep_P0B1_{pose}")
        pose_shapes=[]
        for item in instances:
            xyz=list(item["xyz"])
            if item["moving"] or item["name"].startswith(("prop_screw_","prop_pin_","prop_jack","prop_cap_")):
                xyz[2]+=extension
            rot=item["rotation"]
            loc=cq.Location(cq.Vector(*xyz)) if rot is None else cq.Location(cq.Vector(*xyz),cq.Vector(*rot[0]),rot[1])
            assy.add(shapes[item["id"]],name=item["name"],loc=loc,color=item["color"])
            pose_shapes.append(shapes[item["id"]].located(loc))
        if export:
            assy.save(str(out/"assemblies"/f"FreeStep_P0B1_{pose}.step"))
            compound=cq.Compound.makeCompound(pose_shapes)
            cq.exporters.export(compound,str(out/"views"/f"{pose}.svg"),opt={"width":1000,"height":850,"projectionDir":(1,-1,0.7),"showHidden":False,"strokeWidth":0.5})
            orient_svg(out/"views"/f"{pose}.svg",(1,-1,0.7))
            if pose=="lowered":
                for label,projection in (("front",(0,-1,0)),("side",(1,0,0)),("top",(0,0,1))):
                    cq.exporters.export(compound,str(out/"views"/f"{label}.svg"),opt={"width":1000,"height":850,"projectionDir":projection,"showHidden":False,"strokeWidth":0.5})
                    orient_svg(out/"views"/f"{label}.svg",projection)
        report.append(dict(pose=pose,extension_mm=extension,seat_top_mm=430+extension,upper_pin_mm=centre+extension))

    for pid,meta in definitions.items():
        meta["quantity"]=sum(i["id"]==pid for i in instances)
        if meta["kind"]=="custom":
            if export:
                cq.exporters.export(shapes[pid],str(out/"parts"/(pid+".step")))
                if pid in {x[0] for x in plate_defs}:
                    cq.exporters.export(cq.Workplane("XY").add(shapes[pid]).section(meta["dimensions"][2]/2),str(out/"dxf"/(pid+".dxf")))
            meta["unit_mass_kg"]=meta["volume_mm3"]*P["steel_density_kg_mm3"]
    serial_instances=[{k:v for k,v in i.items() if k!="color"} for i in instances]
    data=dict(parameters=P,parts=list(definitions.values()),instances=serial_instances,poses=report)
    (out/"manifest.json").write_text(json.dumps(data,indent=2)+"\n")
    with (ROOT/"cutlist.csv").open("w",newline="") as f:
        w=csv.writer(f,lineterminator="\n");w.writerow(["Part_ID","Description","Qty","Width_mm","Height_mm","Wall_mm","Cut_Length_mm","Cut","Material"])
        for pid,meta in definitions.items():
            if "section" in meta:
                w.writerow([pid,meta["description"],meta["quantity"],*meta["section"],meta["cut_length"],"square both ends; no mitres",meta["material"]])
    (ROOT/"cad"/"parts_manifest.json").write_text(json.dumps(data,indent=2)+"\n")
    return data, shapes


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--out",type=Path,default=ROOT/"cad"/"generated")
    args=parser.parse_args();d,_=build(args.out)
    print(f"Generated {len(d['parts'])} part definitions, {len(d['instances'])} instances and three STEP poses")
