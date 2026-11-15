# ----- Day 9: The Fake Call -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.15,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
VC=screen_seq("vc",5)
SHOTS=[(0,4.0,(.9,-1.9,.55),(.75,-1.5,.55),(.55,.72,.5),(.55,.72,.5),45),
 (4.0,6.3,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (6.3,10.2,(.25,-1.5,.3),(.3,-1.25,.3),(.38,.2,.28),(.3,-.3,.15),45),
 (10.2,15.2,(.55,-.35,.58),(.55,-.05,.58),(.55,.72,.58),(.55,.72,.58),45),
 (15.2,18.0,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (18.0,40,(.55,-1.3,.5),(.55,-.8,.52),(.55,.72,.52),(.55,.72,.52),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    lv=env("vance",FRi-9); m=0 if lv<.18 else (1 if lv<.55 else 2)   # lips deliberately out of sync
    if t<17.8: im.image=VC[m]
    elif t<20.45:
        g=int(t*14)%5; im.image=VC[3] if (t>18.2 and g!=0) or (t<18.2 and g==0) else VC[m]
    else: im.image=VC[4]
    red_alert(.45*seg(t,18.1,18.4)*(1-seg(t,20.3,20.8)))
    maya.armR.rotation_euler.x=-1.4*seg(t,4.2,4.5)*(1-seg(t,6.4,6.7)) - 2.2*seg(t,15.4,15.7)*(1-seg(t,17.3,17.6))
    maya.H.rotation_euler.z=math.radians(-28)*seg(t,6.4,6.8)*(1-seg(t,15.1,15.4))+.05*math.sin(t*2); maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else (1.4 if t>18.2 else 1)
    clawd.B.location.z=clawd.bounce(t,6.4,.4,.14); clawd.armR.rotation_euler.x=-2.6*seg(t,6.4,6.6)*(1-seg(t,9.8,10.1)) - 2.2*seg(t,10.6,10.8)*(1-seg(t,14.8,15.1))
    clawd.R.rotation_euler.z=math.radians(25)*seg(t,6.4,6.8)*(1-seg(t,15,15.3)); clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(6.3<t<7.5 or t>18.2))
    bit.B.location.z=abs(math.sin(t*28))*.004*(t>18); bit.eyes_set(t,.7,wide=(t>18.2)); bit.talk("bit",FRi)
render_loop(animate)
