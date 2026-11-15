# ----- Day 7: Memory -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.15,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
DK=mat("dark",(.02,.02,.025),.4)
fb=boxo("fBase",(-.7,-.25,.006),(.34,.24,.012),DK)
lidR=rig("lidR",(-.7,-.13,.012)); lid=boxo("fLid",(0,-.12,.004),(.34,.24,.008),DK); lid.parent=lidR
ring=[]
for a in range(0,300,15):
    ang=math.radians(a+40); ring.append(((math.cos(ang)*.05,-.12+math.sin(ang)*.05,.01),(.016,.016,.006)))
part("sym",ring,mat("symr",(1,.05,.05),.3,em=14,emc=(1,.05,.05)),lidR)
glow=boxo("glow",(-.7,-.25,.014),(.3,.2,.002),mat("glowm",(1,.1,.1),.3)); glow.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value=(1,.08,.05,1)
bpy.ops.object.light_add(type='POINT',location=(-.7,-.3,.25)); RL=bpy.context.object; RL.data.color=(1,.08,.05); RL.data.energy=0
NC=screen_seq("nc",1); ME=screen_seq("me",25); UN=screen_seq("un",13); PH=screen_seq("ph",1)
SHOTS=[(0,3.1,(.25,-1.3,.25),(.28,-1.1,.24),(.3,-.3,.17),(.3,-.3,.15),50),
 (3.1,7.6,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (7.6,13.7,(.6,-1.9,.5),(.6,-1.4,.52),(.55,.72,.5),(.55,.72,.5),45),
 (13.7,16.4,(.1,-1.8,.35),(.12,-1.55,.33),(.08,-.3,.15),(.1,-.3,.15),38),
 (16.4,19.4,(-.45,-1.2,.38),(-.58,-.95,.32),(-.7,-.25,.1),(-.7,-.25,.1),50),
 (19.4,40,(.55,-1.7,.48),(.55,-.95,.52),(.55,.72,.52),(.55,.72,.52),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    if t<7.6: im.image=NC[0] if t>3.3 else bpy.data.images["screen.png"]
    elif t<16.6: im.image=ME[int(seg(t,7.8,13.0)*24)]
    elif t<19.2: im.image=UN[int(seg(t,16.7,18.8)*12)]
    else: im.image=PH[0]
    # folder opens by itself with red light
    lidR.rotation_euler.x=-1.9*eo(seg(t,17.2,18.4))+ .04*math.sin(t*40)*(16.6<t<17.2)
    g=seg(t,17.3,18.4); glow.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value=18*g; RL.data.energy=60*g*(.8+.2*math.sin(t*25))
    red_alert(.3*seg(t,18.6,19.4))
    # Maya explains, gestures
    maya.armR.rotation_euler.x=-1.6*seg(t,3.4,3.7)*(1-seg(t,7.2,7.5)) - (1.2+.3*math.sin(t*5))*(7.8<t<13.4)
    maya.H.rotation_euler.z=math.radians(-22)*seg(t,3.2,3.5)*(1-seg(t,13.4,13.8)) + .05*math.sin(t*2)
    maya.R.location.z=-.15+.03*math.sin(t*1.3); maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else 1
    # Clawd: sad look up, then nods, then shocked
    clawd.H=None
    clawd.R.rotation_euler.z=math.radians(-30)*seg(t,3.2,3.6)*(1-seg(t,13.6,13.9)) + math.radians(30)*seg(t,19.4,19.8)
    clawd.B.rotation_euler.x=-.15*seg(t,.3,.8)*(1-seg(t,3,3.4)) + .1*math.sin(t*9)*(14.0<t<14.8)
    clawd.armR.rotation_euler.x=-2.2*seg(t,14.6,14.8)*(1-seg(t,15.8,16.1))
    clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t>19.5)); clawd.B.location.z=clawd.bounce(t,14.6,.35,.08)
    # Bit points at the folder
    bit.R.rotation_euler.z=math.radians(-40)*seg(t,16.5,16.8); bit.armL.rotation_euler.x=-2.4*seg(t,16.7,16.9)*(1-seg(t,19,19.3))
    bit.B.location.z=bit.bounce(t,14.9,.35,.08)+abs(math.sin(t*28))*.004*(t>17)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t>16.6))
render_loop(animate)
