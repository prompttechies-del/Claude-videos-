# ----- Day 11: Lockdown -----
clawd=Toon("clawd",(-.3,-.3,0),ORA)
bit=Toon("bit",(-.05,-.35,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
AP=screen_seq("ap",9)
SHOTS=[(0,2.2,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (2.2,7.95,(-.1,-1.8,.4),(.0,-1.5,.38),(-.05,-.1,.18),(-.2,-.3,.15),38),
 (7.95,13.0,(.3,-1.8,.5),(.45,-1.3,.52),(.55,.72,.5),(.55,.72,.5),45),
 (13.0,15.35,(.25,-.8,.25),(.22,-.68,.22),(.2,.1,.1),(.2,.1,.1),50),
 (15.35,17.6,(.55,-1.4,.5),(.55,-.85,.52),(.55,.72,.52),(.55,.72,.52),50),
 (17.6,40,(-.32,-1.25,.24),(-.3,-1.05,.23),(-.3,-.3,.17),(-.3,-.3,.15),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    n=0 if t<13.2 else min(5,1+int((t-13.2)/.35)); n=7 if t>15.0 else n
    im.image=AP[8] if t>15.6 else AP[n]
    alarm=(.5+.5*math.sin(t*12))*(1-seg(t,13.2,15.0)) if t<15.0 else 0
    red_alert(.75*alarm+.4*seg(t,15.6,16.0))
    # Bit runs to the keyboard and types
    run=ease(seg(t,3.0,3.8)); bp=Vector((-.05,-.35,0)).lerp(Vector((.2,.1,.035)),run); bp.z+=math.sin(run*math.pi)*.15; bit.R.location=bp
    typing_=(4.0<t<15.1); bit.armL.rotation_euler.x=-(1.0+.6*math.sin(t*22))*typing_; bit.armR.rotation_euler.x=-(1.0+.6*math.sin(t*22+2))*typing_ - 2.4*seg(t,14.6,14.8)*(1-seg(t,15.3,15.5))
    bit.B.location.z=abs(math.sin(t*11))*.012*typing_+bit.bounce(t,14.7,.35,.1); bit.R.rotation_euler.z=math.radians(150)*seg(t,15.4,15.8)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t<3 or t>15.5))
    # Clawd commands
    clawd.armR.rotation_euler.x=-2.4*seg(t,2.4,2.6)*(1-seg(t,7.4,7.7)); clawd.armL.rotation_euler.x=-1.4*seg(t,8.3,8.5)*(1-seg(t,12.5,12.8))
    clawd.R.rotation_euler.z=math.radians(-20)*seg(t,2.3,2.6)*(1-seg(t,7.8,8.1))+math.radians(30)*seg(t,8.1,8.5)*(1-seg(t,12.9,13.2))
    clawd.B.location.z=clawd.bounce(t,.4,.4,.12); clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t<2.2 or t>17.0))
    clawd.B.rotation_euler.x=-.15*seg(t,17.8,18.4)
    maya.armL.rotation_euler.x=maya.armR.rotation_euler.x=-2.6*seg(t,.3,.5)*(1-seg(t,2.0,2.3))
    maya.R.location.z=-.15+.03*math.sin(t*1.3)+abs(math.sin(t*12))*.02*(t<2.2); maya.talk("maya",FRi); maya.eyes.scale.z=1.4 if t<2.5 else (.12 if blink(t,.4) else 1)
render_loop(animate)
