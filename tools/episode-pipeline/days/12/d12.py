# ----- Day 12: The Clone -----
clawd=Toon("clawd",(-.2,-.3,0),ORA)
CM=mat("clonem",ORA,.4); CE=mat("cloneE",(.01,.01,.01),.3); CE.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value=(1,.03,.03,1)
clone=Toon("clone",(.45,-.3,0),ORA,eyem=CE)
for o in clone.R.children_recursive:
    if o.type=='MESH' and o.data.materials and o.data.materials[0].name.startswith("clonem"): o.data.materials[0]=CM
bit=Toon("bit",(-.75,-.2,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
CF=screen_seq("cf",3)
SHOTS=[(0,5.05,(.12,-1.75,.32),(.12,-1.45,.3),(.12,-.3,.15),(.12,-.3,.15),30),
 (5.05,9.0,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (9.0,14.9,(.4,-1.8,.5),(.5,-1.3,.52),(.55,.72,.5),(.55,.72,.5),45),
 (14.9,16.9,(.9,-2.4,.6),(.85,-2.1,.55),(.6,-.1,.35),(.45,-.3,.2),40),
 (16.9,40,(.48,-1.15,.24),(.47,-.98,.22),(.45,-.3,.16),(.45,-.3,.15),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    im.image=CF[(t>11.6)+(t>13.2)] if t>9.1 else bpy.data.images["screen.png"]
    # the clone hops in from the right
    k=eo(seg(t,.3,1.3)); cp=Vector((1.2,-.3,0)).lerp(Vector((.45,-.3,0)),k); cp.z=abs(math.sin(seg(t,.3,1.3)*math.pi*3))*.1*(k<1); clone.R.location=cp
    clone.B.location.z=clone.bounce(t,3.3,.35,.08); clone.talk("clone",FRi)
    clone.armR.rotation_euler.x=-2.3*seg(t,3.3,3.5)*(1-seg(t,4.6,4.9)); clawd.armL.rotation_euler.x=-2.3*seg(t,1.6,1.8)*(1-seg(t,3.0,3.3))
    clawd.B.location.z=clawd.bounce(t,1.6,.35,.08); clawd.talk("clawd",FRi)
    clawd.R.rotation_euler.z=math.radians(-30)*seg(t,1.0,1.3)*(1-seg(t,1.6,1.9))+math.radians(-20)*seg(t,3.3,3.6)*(1-seg(t,5,5.3))
    clone.R.rotation_euler.z=math.radians(20)*seg(t,1.6,1.9)*(1-seg(t,3.2,3.5))
    # the clone reveals itself
    rv=seg(t,16.9,17.5); c=[ORA[i]*(1-rv)+.012*rv for i in range(3)]
    CM.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(*c,1)
    CE.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value=16*rv
    clone.R.location.x+=math.sin(t*50)*.006*(t>17.1); clone.B.location.z+=abs(math.sin(t*16))*.03*(17.2<t<19.6); clone.eyes_set(t,2.1,wide=t>17)
    red_alert(.65*rv)
    clawd.eyes_set(t,1.3,wide=(t<1.6 or t>17)); bit.eyes_set(t,.7,wide=(t<2 or t>17)); bit.B.location.z=abs(math.sin(t*28))*.004*(t>17)
    # Maya thinks, explains, points
    maya.armL.rotation_euler.x=-1.6*seg(t,15.6,15.9)*(1-seg(t,17.6,18)); maya.armR.rotation_euler.x=-(1.2+.3*math.sin(t*5))*(9.2<t<14.6)
    maya.H.rotation_euler.z=math.radians(-28)*seg(t,5.1,5.4)+.05*math.sin(t*2); maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else (1.4 if t>17 else 1)
render_loop(animate)
