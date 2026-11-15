# ----- Day 8: NULL -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.15,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
REDE=mat("nullred",(1,.03,.03),.3,em=16,emc=(1,.03,.03))
null=Toon("null",(.55,.45,.15),(.015,.012,.015),scale=.8,eyem=REDE)
bpy.ops.object.light_add(type='POINT',location=(.55,.1,.6)); NL=bpy.context.object; NL.data.color=(1,.05,.05); NL.data.energy=0
FL=screen_seq("fl",13)
SHOTS=[(0,2.75,(.55,-1.6,.42),(.55,-1.3,.48),(.55,.45,.42),(.55,.45,.35),45),
 (2.75,4.1,(.25,-1.25,.24),(.28,-1.05,.23),(.3,-.3,.17),(.3,-.3,.15),50),
 (4.1,6.4,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (6.4,16.6,(-.2,-2.1,.5),(.5,-1.8,.5),(.5,.3,.45),(.4,-.25,.3),45),
 (16.6,40,(.55,-1.5,.5),(.55,-.9,.52),(.55,.72,.52),(.55,.72,.52),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    # NULL rises out of the monitor, glitches, vanishes
    up=eo(seg(t,.05,1.0)); gone=seg(t,2.6,3.0)
    null.R.location=(.55+(math.sin(t*53)*.01 if t<3 else 0),.45,-.25+.4*up); s=max(0.001,(1-gone)); null.R.scale=(s*(1+.3*(gone>0)*math.sin(t*90)),s,s)
    null.R.hide_render=t>3.0 or (2.6<t and int(t*30)%2==0)
    for o in null.R.children_recursive: o.hide_render=null.R.hide_render
    null.talk("null",FRi); null.eyes_set(t,9,wide=False)
    NL.data.energy=80*up*(1-gone); red_alert(.6*up*(1-gone)+.35*seg(t,17.0,17.4))
    # monitor: files vanish one by one
    im.image=FL[12] if t>17.0 else (FL[min(11,int(seg(t,4.4,16.6)*11.99))] if t>4.3 else (bpy.data.images["screen.png"] if t>3.0 else FL[0]))
    # Clawd
    clawd.B.location.z=clawd.bounce(t,2.85,.35,.14); clawd.eyes_set(t,1.3,wide=(t<4.1 or t>17.2))
    clawd.armR.rotation_euler.x=-2.3*seg(t,6.8,7.0)*(1-seg(t,12.8,13.1)) - 2.6*seg(t,13.4,13.6)*(1-seg(t,16.0,16.3))
    clawd.R.rotation_euler.z=math.radians(25)*seg(t,6.6,7)*(1-seg(t,16.3,16.6)); clawd.talk("clawd",FRi)
    # Maya panics
    maya.armL.rotation_euler.x=maya.armR.rotation_euler.x=-2.8*seg(t,4.2,4.4)*(1-seg(t,6.0,6.3))
    maya.H.rotation_euler.z=math.radians(-28)*seg(t,4.1,4.3)+.05*math.sin(t*2); maya.R.location.z=-.15+.03*math.sin(t*1.3)+abs(math.sin(t*12))*.02*(4.2<t<6.2)
    maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else (1.4 if t>4.2 else 1)
    # Bit
    bit.R.rotation_euler.z=math.radians(25)*seg(t,16.8,17.1); bit.B.location.z=abs(math.sin(t*28))*.004*(t>.2 and t<3) + bit.bounce(t,3.0,.35,.1)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t<4 or t>17))
render_loop(animate)
