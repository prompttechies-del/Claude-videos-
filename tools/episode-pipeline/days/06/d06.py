# ----- Day 6: The Symbol -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.15,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
# file box with folders
v=.03; part("fbox",[c for c in vox_box(-.95,-.55,-.25,.05,0,.18,v) if c[0][2]<.16],mat("fbox",(.35,.22,.12),.6),None)
FC=[(.9,.3,.2),(.2,.5,.9),(.95,.75,.2),(.3,.75,.4),(.8,.4,.8),(.9,.55,.3),(.4,.8,.85),(.85,.85,.8)]
R_=random.Random(4); folders=[]
for i,c in enumerate(FC):
    o=boxo("fold%d"%i,(0,0,0),(.3,.012,.2),mat("fold%d"%i,c,.6)); o.location=(-.75,-.2+i*.03,.12)
    folders.append((o,Vector(o.location),Vector((R_.uniform(-1.4,-.1),R_.uniform(-.7,.3),.02)),Vector((R_.uniform(-2,2),R_.uniform(-.5,.5),R_.uniform(0,6))),4.3+i*.18))
DK=mat("dark",(.02,.02,.025),.4)
dark=rig("darkR",(-.75,-.1,.05)); boxo("darkF",(0,0,0),(.32,.014,.22),DK).parent=dark
ring=[]
for a in range(0,300,15):
    ang=math.radians(a+40); ring.append(((math.cos(ang)*.06,-.012,math.sin(ang)*.06+.01),(.018,.006,.018)))
part("sym",ring,mat("symr",(1,.05,.05),.3,em=14,emc=(1,.05,.05)),dark)
tv=text3d("v0.1",(0,-.012,-.085),size=.04,col=(.85,.85,.9),em=2); tv.parent=dark; tv.location=(0,-.012,-.085)
SYM=screen_seq("sym",1); DOC=screen_seq("doc",7); LK=screen_seq("lk",25)
SHOTS=[(0,2.5,(.25,-1.6,.32),(.3,-1.35,.32),(.38,.2,.3),(.3,-.3,.15),45),
 (2.5,3.8,(.2,-1.3,.25),(.25,-1.15,.22),(.3,-.2,.12),(.4,-.15,.1),50),
 (3.8,6.2,(-1.1,-1.6,.6),(-.6,-1.6,.55),(-.75,-.1,.15),(-.75,-.1,.15),45),
 (6.2,13.4,(.4,-1.8,.5),(.5,-1.3,.52),(.55,.72,.5),(.55,.72,.5),45),
 (13.4,17.6,(-.6,-1.3,.35),(-.68,-1.0,.38),(-.75,-.25,.35),(-.75,-.25,.35),50),
 (17.6,40,(.2,-1.5,.35),(.3,-1.15,.36),(.4,.2,.32),(.3,-.3,.15),45)]
def animate(t,FRi):
    camera(t,SHOTS)
    if t<6.2: im.image=SYM[0]
    elif t<16.3: im.image=DOC[0 if t<8.6 else min(6,1+int((t-8.6)/.45)) if t<11.0 else (5 if t<11.3 else 6)]
    else: im.image=LK[int(seg(t,16.4,18.4)*24)]
    # Bit hides behind Clawd, later spots the folder
    hide=eo(seg(t,2.55,2.95))*(1-eo(seg(t,3.9,4.3))); bit.R.location=Vector((-.15,-.3,0)).lerp(Vector((.55,-.12,0)),hide)
    bit.R.rotation_euler.z=math.radians(160)*seg(t,2.55,2.7)*(1-seg(t,2.9,3.05)) + math.radians(30)*seg(t,13.4,13.7)
    bit.B.location.z=bit.bounce(t,13.55,.35,.12)+abs(math.sin(t*30))*.004*(2.6<t<3.6)
    bit.armR.rotation_euler.x=-2.4*seg(t,13.6,13.8)*(1-seg(t,15.8,16.1))
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(2.5<t<3.8 or 13.5<t<14.5))
    # Clawd
    clawd.R.rotation_euler.z=math.radians(-25)*seg(t,2.5,2.8)*(1-seg(t,3.8,4.1)) + math.radians(-35)*seg(t,4.0,4.4)*(1-seg(t,6.0,6.3)) + math.radians(30)*seg(t,6.3,6.7)*(1-seg(t,13.2,13.5)) + math.radians(-35)*seg(t,13.6,14)*(1-seg(t,17.4,17.8))
    clawd.armR.rotation_euler.x=-2.3*seg(t,6.4,6.6)*(1-seg(t,12.9,13.2)); clawd.armL.rotation_euler.x=-1.5*seg(t,.4,.6)*(1-seg(t,2.0,2.3))
    clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t>19.0)); clawd.B.location.z=clawd.bounce(t,4.0,.35,.08)
    # folders fly out of the box and land around it
    for o,p0,p1,rot,t0 in folders:
        kf=seg(t,t0,t0+.6); p=p0.lerp(p1,ease(kf)); p.z+=math.sin(kf*math.pi)*.5; o.location=p
        o.rotation_euler=Vector((math.pi/2*ease(kf),0,0))+rot*ease(kf)*.3 if kf>0 else Vector((0,0,0))
    # the dark folder rises with its red symbol
    kd=eo(seg(t,13.5,14.3)); dark.location=Vector((-.75,-.1,.05)).lerp(Vector((-.75,-.25,.35)),kd); dark.hide_render=t<13.45
    for ch in dark.children: ch.hide_render=t<13.45
    dark.rotation_euler.z=math.sin(t*1.5)*.15*kd
    fl=.4*seg(t,16.4,16.7)*(.6+.4*(int(t*9)%3!=0)) if t>16.4 else 0; red_alert(fl)
render_loop(animate)
