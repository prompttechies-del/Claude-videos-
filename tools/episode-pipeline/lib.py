# Photoreal desk scene with a voxel Clawd, for Prompt Techies Reels. Usage: blender -b -P desk.py -- ENGINE W H SAMPLES OUT FRAME
import bpy, bmesh, math, sys, random
from mathutils import Vector
a=sys.argv[sys.argv.index("--")+1:]; ENG,W,H,SAMP,OUT,FR=a[0],int(a[1]),int(a[2]),int(a[3]),a[4],int(a[5])
bpy.ops.wm.read_factory_settings(use_empty=True); sc=bpy.context.scene; random.seed(3)
def mat(name,col,rough=.5,em=0,emc=None,metal=0,tex=None):
    m=bpy.data.materials.new(name); m.use_nodes=True; n=m.node_tree.nodes; b=n["Principled BSDF"]
    b.inputs["Base Color"].default_value=(*col,1); b.inputs["Roughness"].default_value=rough; b.inputs["Metallic"].default_value=metal
    if em: b.inputs["Emission Color"].default_value=(*(emc or col),1); b.inputs["Emission Strength"].default_value=em
    if tex=="wood":
        L=m.node_tree.links; tc=n.new("ShaderNodeTexCoord"); mp=n.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value=(.6,9,.6)
        w=n.new("ShaderNodeTexWave"); w.wave_type='BANDS'; w.inputs["Scale"].default_value=3; w.inputs["Distortion"].default_value=2.5; w.inputs["Detail"].default_value=6
        r=n.new("ShaderNodeValToRGB"); r.color_ramp.elements[0].color=(.16,.07,.03,1); r.color_ramp.elements[1].color=(.42,.2,.09,1)
        L.new(tc.outputs["Object"],mp.inputs["Vector"]); w.bands_direction="Y"; L.new(mp.outputs["Vector"],w.inputs["Vector"]); L.new(w.outputs["Fac"],r.inputs["Fac"]); L.new(r.outputs["Color"],b.inputs["Base Color"])
    return m
def obj(name,bm,m):
    me=bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); o=bpy.data.objects.new(name,me); sc.collection.objects.link(o); o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth=False
    return o
def cube(bm,c,s):
    r=bmesh.ops.create_cube(bm,size=1); bmesh.ops.scale(bm,vec=s,verts=r["verts"]); bmesh.ops.translate(bm,vec=c,verts=r["verts"])
def boxo(name,c,s,m,bev=0):
    bm=bmesh.new(); cube(bm,c,s); o=obj(name,bm,m)
    if bev: md=o.modifiers.new("b","BEVEL"); md.width=bev; md.segments=3
    return o
# desk, wall, props
boxo("desk",(0,0,-.03),(4,2,.06),mat("wood",(.4,.2,.1),.35,tex="wood"))
boxo("wall",(0,1.6,1),(8,.05,4),mat("wall",(.16,.11,.2),.9))
mon=boxo("mon",(.55,.75,.52),(1.1,.04,.66),mat("bez",(.02,.02,.025),.4),.01)
scr=bpy.data.materials.new("scr"); scr.use_nodes=True; nn=scr.node_tree.nodes; L=scr.node_tree.links; nn.remove(nn["Principled BSDF"])
em=nn.new("ShaderNodeEmission"); em.inputs["Strength"].default_value=3.5; im=nn.new("ShaderNodeTexImage"); im.image=bpy.data.images.load(bpy.path.abspath("//screen.png")); tc=nn.new("ShaderNodeTexCoord"); mp=nn.new("ShaderNodeMapping")
mp.inputs["Rotation"].default_value=(math.pi/2,0,0); L.new(tc.outputs["Generated"],mp.inputs["Vector"]); L.new(mp.outputs["Vector"],im.inputs["Vector"]); L.new(im.outputs["Color"],em.inputs["Color"]); L.new(em.outputs["Emission"],nn["Material Output"].inputs["Surface"])
boxo("scr",(.55,.725,.52),(1.02,.01,.58),scr)
boxo("stand",(.55,.8,.12),(.08,.05,.24),mat("bez2",(.03,.03,.03),.3))
mug=bpy.ops.mesh.primitive_cylinder_add(radius=.13,depth=.3,location=(-.95,.15,.15)); mg=bpy.context.object; mg.data.materials.append(mat("mug",(.95,.45,.6),.2)); bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_torus_add(major_radius=.08,minor_radius=.02,location=(-1.1,.15,.16),rotation=(math.pi/2,0,0)); bpy.context.object.data.materials.append(mg.data.materials[0])
boxo("kb",(.1,.1,.02),(.8,.25,.03),mat("kb",(.85,.85,.82),.4),.008)
leafm=mat("lf",(.03,.22,.05),.5)
for i in range(130):
    bpy.ops.mesh.primitive_plane_add(size=.14,location=(-1.0+random.gauss(0,.2),1.25+random.gauss(0,.12),.55+random.random()*.9),rotation=(random.random()*3,random.random()*3,random.random()*3))
    o=bpy.context.object; o.scale=(.35,1,1); o.data.materials.append(leafm)
bpy.ops.mesh.primitive_cylinder_add(radius=.16,depth=.35,location=(-1.0,1.25,.17)); bpy.context.object.data.materials.append(mat("pot",(.85,.35,.25),.6))
# neon sign on the wall
bpy.ops.mesh.primitive_torus_add(major_radius=.28,minor_radius=.018,location=(.35,1.55,1.45),rotation=(math.pi/2,0,0)); bpy.context.object.data.materials.append(mat("neon",(1,.15,.5),.3,em=25,emc=(1,.15,.55)))
boxo("neon2",(.35,1.55,1.05),(.7,.02,.035),mat("neon2",(.1,.9,1),.3,em=25,emc=(.1,.9,1)))
# lights behind for bokeh dots
for i in range(18):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.035,location=(-2.4+i*.3,1.5,.55+random.random()*1.4)); cc=[(1,.45,.15),(1,.2,.55),(.15,.85,1),(.7,.3,1),(1,.8,.3)][i%5]; bpy.context.object.data.materials.append(mat("bk",cc,.5,em=40,emc=cc))
# lighting and world
bpy.ops.object.light_add(type='AREA',location=(-2,-1.5,2.5)); k=bpy.context.object; k.data.energy=200; k.data.size=2; k.data.color=(1,.82,.62); k.rotation_euler=(math.radians(50),0,math.radians(-50))
bpy.ops.object.light_add(type='AREA',location=(2,1.2,1.2)); r=bpy.context.object; r.data.energy=260; r.data.size=1; r.data.color=(.2,.85,1); r.rotation_euler=(math.radians(-70),0,math.radians(120))
bpy.ops.object.light_add(type='AREA',location=(-1.8,1.0,1.0)); f=bpy.context.object; f.data.energy=150; f.data.size=1.2; f.data.color=(1,.25,.6); f.rotation_euler=(math.radians(-80),0,math.radians(-120))
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs["Color"].default_value=(.015,.012,.01,1)
bpy.ops.object.camera_add(); cam=bpy.context.object; sc.camera=cam; cam.data.lens=70; cam.data.sensor_width=36
cam.data.dof.use_dof=True; cam.data.dof.focus_distance=3; cam.data.dof.aperture_fstop=0.95
sc.render.engine=ENG; sc.render.resolution_x=W; sc.render.resolution_y=H; sc.render.filepath=OUT
sc.view_settings.view_transform='Filmic'; sc.view_settings.look='High Contrast'; sc.view_settings.exposure=.05
if ENG=="CYCLES": sc.cycles.samples=SAMP; sc.cycles.use_denoising=False; sc.cycles.max_bounces=4
else:
    e=sc.eevee; e.taa_render_samples=SAMP; e.use_bloom=True; e.bloom_intensity=.12; e.use_soft_shadows=True; e.use_gtao=True; e.use_ssr=True; e.shadow_cube_size='1024'; e.shadow_cascade_size='1024'
# ===== shared episode library =====
import json, os
DAY=os.environ["DAY"]; TM=json.load(open(bpy.path.abspath(f"//v{DAY}/timing.json"))); ENV=TM["env"]; FPS=24
def env(who,f): e=ENV.get(who,[]); return e[f] if 0<=f<len(e) else 0
def ease(k): k=max(0,min(1,k)); return k*k*(3-2*k)
def eo(k): k=max(0,min(1,k)); return 1-(1-k)**3
def seg(t,a,b): return max(0,min(1,(t-a)/(b-a)))
def blink(t,s): return ((t+s)%3.1)<.12
def rig(name,loc,parent=None):
    e=bpy.data.objects.new(name,None); sc.collection.objects.link(e); e.location=loc; e.parent=parent; return e
def part(name,cubes,m,parent,origin=(0,0,0)):
    bm=bmesh.new()
    for c,s in cubes: cube(bm,(c[0]-origin[0],c[1]-origin[1],c[2]-origin[2]),s)
    o=obj(name,bm,m); o.parent=parent; o.location=origin; return o
def vox_box(x0,x1,y0,y1,z0,z1,v,shell=True):
    out=[]; nx,ny,nz=round((x1-x0)/v),round((y1-y0)/v),round((z1-z0)/v)
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if shell and 0<i<nx-1 and 0<j<ny-1 and 0<k<nz-1: continue
                out.append(((x0+(i+.5)*v,y0+(j+.5)*v,z0+(k+.5)*v),(v*.94,v*.94,v*.94)))
    return out
def text3d(s,loc,size=.075,col=(1,1,1),em=4,rot=(math.pi/2,0,0),name=None):
    global FNT
    try: FNT
    except NameError: FNT=bpy.data.fonts.load(bpy.path.abspath("//../mg/assets/BigShoulders-Bold.ttf"))
    cu=bpy.data.curves.new(name or s,"FONT"); cu.body=s; cu.font=FNT; cu.size=size; cu.align_x='CENTER'; cu.extrude=.004
    o=bpy.data.objects.new(name or s,cu); sc.collection.objects.link(o); o.location=loc; o.rotation_euler=rot
    o.data.materials.append(mat("t_"+s,col,.4,em=em,emc=col)); return o
BLK=mat("blk",(.01,.01,.01),.3)
class Toon:  # a voxel box character (Clawd, NULL, Bit)
    def __init__(s,name,loc,col,scale=.55,eye=None,eyem=None,W=13,D=9,Hh=9,antenna=False):
        s.R=rig(name+"R",loc); s.B=rig(name+"B",(0,0,0),s.R); s.CS=scale; V=.045*scale; s.V=V
        body=vox_box(-W*V/2,W*V/2,-D*V/2,D*V/2,3*V,(3+Hh)*V,V)
        legs=[((x*V-W*V/2+V/2,0,z*V+V/2),(V*.93,)*3) for x in (1,4,W-5,W-2) for z in range(3)]
        arms=[((sd*(W/2+.5)*V,0,(z+3)*V+V/2+2*V),(V*.93,)*3) for sd in (-1,1) for z in range(2)]
        M=mat(name+"m",col,.4); part(name+"Body",body+legs,M,s.B)
        EM=eyem or BLK; ez=(3+Hh*.47)*V
        s.eyes=part(name+"Eyes",[((x*V,-D*V/2-V*.3,ez),(V*.95,V*.6,V*1.9)) for x in (-3,3)],EM,s.B,(0,-D*V/2,ez))
        s.armL=part(name+"ArmL",arms[:2],M,s.B,(-W*V/2,0,6*V)); s.armR=part(name+"ArmR",arms[2:],M,s.B,(W*V/2,0,6*V))
        mz=(3+Hh*.21)*V
        s.mouth=[part(name+"M%d"%i,[((0,-D*V/2-V*.3,mz),(V*w,V*.6,V*h))],EM if eyem else BLK,s.B,(0,-D*V/2,mz)) for i,(w,h) in enumerate([(3,.45),(2.2,1.2),(2.6,2.2)])]
        if antenna:
            part(name+"Ant",[((0,0,(3+Hh)*V+i*V+V/2),(V*.5,V*.5,V*.93)) for i in range(3)],M,s.B)
            s.tip=part(name+"Tip",[((0,0,(6+Hh)*V+V*.6),(V*1.3,)*3)],mat(name+"tip",(1,.9,.2),.3,em=12,emc=(1,.85,.2)),s.B)
    def talk(s,who,FRi,force=None):
        lv=env(who,FRi) if force is None else force; l=0 if lv<.18 else (1 if lv<.55 else 2)
        for i,o in enumerate(s.mouth): o.hide_render=(i!=l)
    def eyes_set(s,t,ph,wide=False,shut=False):
        s.eyes.scale.z=.12 if (shut or (blink(t,ph) and not wide)) else (1.5 if wide else 1)
    def bounce(s,t,t0,dur=.4,h=.1):
        k=seg(t,t0,t0+dur); return math.sin(k*math.pi)*h
class Human:
    def __init__(s,name,loc,shirt=(.12,.42,.72),hair=(.05,.03,.02),skin=(.78,.52,.38),tie=None):
        s.R=rig(name+"R",loc); u=.05
        SK=mat(name+"sk",skin,.55); SH=mat(name+"sh",shirt,.6); HR=mat(name+"hr",hair,.5); WH=mat("white",(.95,.95,.95),.3)
        part(name+"Torso",vox_box(-.2,.2,-.1,.1,0,.6,u),SH,s.R)
        if tie: part(name+"Tie",[((0,-.103,.42),(.05,.01,.3))],mat(name+"tie",tie,.4),s.R)
        s.H=rig(name+"Head",(0,0,.62),s.R)
        part(name+"HeadM",vox_box(-.15,.15,-.15,.15,0,.3,u),SK,s.H)
        part(name+"Hair",vox_box(-.17,.17,-.05,.17,.22,.36,u)+vox_box(-.17,.17,.1,.17,-.05,.3,u),HR,s.H)
        s.eyes=part(name+"Eyes",[((x,-.158,.17),(.045,.012,.05)) for x in (-.07,.07)],BLK,s.H,(0,-.158,.17))
        part(name+"EyeW",[((x,-.155,.17),(.07,.01,.06)) for x in (-.07,.07)],WH,s.H)
        s.mouth=[part(name+"M%d"%i,[((0,-.158,.075),(w,.012,h))],BLK,s.H,(0,-.158,.075)) for i,(w,h) in enumerate([(.07,.012),(.06,.03),(.07,.055)])]
        s.armL=part(name+"ArmL",vox_box(-.3,-.2,-.05,.05,.1,.55,u,False),SH,s.R,(-.25,0,.55)); s.armR=part(name+"ArmR",vox_box(.2,.3,-.05,.05,.1,.55,u,False),SH,s.R,(.25,0,.55))
        for a,x in ((s.armL,-.25),(s.armR,.25)):
            hh=part(a.name+"H",[((x,0,.08),(.09,.09,.09))],SK,a,(x,0,.55)); hh.location=(0,0,0)
    def talk(s,who,FRi):
        lv=env(who,FRi); l=0 if lv<.18 else (1 if lv<.55 else 2)
        for i,o in enumerate(s.mouth): o.hide_render=(i!=l)
ORA=(.72,.13,.015)
def screen_seq(prefix,n): return [bpy.data.images.load(bpy.path.abspath(f"//v{DAY}/{prefix}_{i:02d}.png")) for i in range(n)]
LIGHTS=[k,r,f]; LBASE=[(l.data.energy,tuple(l.data.color)) for l in LIGHTS]
def red_alert(level):  # 0 normal .. 1 full red
    for l,(e0,c0) in zip(LIGHTS,LBASE):
        l.data.color=tuple(c0[i]*(1-level)+(1,.05,.05)[i]*level for i in range(3)); l.data.energy=e0*(1+.5*level)
def camera(t,SHOTS):
    for sh in SHOTS:
        a0,a1,p0,p1,lk,fc=sh[:6]
        if t<a1: break
    lens=sh[6] if len(sh)>6 else 55
    kk=ease((t-a0)/(a1-a0)); cp=Vector(p0).lerp(Vector(p1),kk); cp.x+=math.exp(-(t-a0)*9)*.12*(1 if a0 else 0)
    cam.location=cp; cam.rotation_euler=(Vector(lk)-cp).to_track_quat('-Z','Y').to_euler(); cam.data.dof.focus_distance=(Vector(fc)-cp).length; cam.data.lens=lens
    return a0
def render_loop(animate):
    for FRi in range(FR, FR+int(os.environ.get("NFR","1"))):
        animate(FRi/FPS,FRi); sc.render.filepath=OUT.replace("#","%04d"%FRi); bpy.ops.render.render(write_still=True)
