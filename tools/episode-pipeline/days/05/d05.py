# ----- Day 5: Why AI Images Look Fake -----
clawd=Toon("clawd",(.35,-.3,0),ORA)
bit=Toon("bit",(-.2,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
BAD=screen_seq("bad",4); GOOD=screen_seq("good",2)
SHOTS=[(0,3.5,(1.3,-2.4,.7),(1.1,-2.0,.65),(1.0,.4,.55),(1.4,.25,.6),45),
 (3.5,5.1,(-.15,-1.0,.2),(-.17,-.85,.18),(-.2,-.3,.12),(-.2,-.3,.12),55),
 (5.1,7.75,(.3,-1.7,.35),(.35,-1.45,.35),(.35,-.3,.2),(.35,-.3,.15),50),
 (7.75,8.55,(.42,-.05,.48),(.42,.12,.48),(.42,.72,.48),(.42,.725,.48),50),
 (8.55,9.3,(.77,-.1,.57),(.77,.05,.57),(.77,.72,.57),(.77,.725,.57),50),
 (9.3,10.35,(.41,-.05,.32),(.41,.1,.32),(.41,.72,.32),(.41,.725,.32),50),
 (10.35,17.3,(-.2,-2.1,.5),(.5,-1.8,.5),(.5,.3,.45),(.45,-.2,.3),45),
 (17.3,20.2,(1.7,-1.9,.75),(1.55,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (20.2,40,(1.0,-.7,.3),(1.0,.42,.28),(.99,.72,.29),(.99,.725,.29),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    # monitor: bad poster with red rings, then the fixed poster
    if t<15.6: im.image=BAD[(t>7.8)+(t>8.6)+(t>9.3)]
    else: im.image=GOOD[1]
    # Maya: proud, then amazed
    maya.armR.rotation_euler.x=-2.2*seg(t,.4,.7)*(1-seg(t,3.0,3.3)); maya.armL.rotation_euler.x=-1.6*seg(t,17.5,17.8)*(1-seg(t,19.3,19.6))
    maya.H.rotation_euler.z=math.radians(-25)*seg(t,3.6,4.0)*(1-seg(t,17.2,17.5)) + .05*math.sin(t*2)
    maya.R.location.z=-.15+.03*math.sin(t*1.3); maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else (1.4 if 3.7<t<5 or 17.4<t<18.4 else 1)
    # Bit screams and jumps, later points
    bit.B.location.z=bit.bounce(t,3.62,.45,.16)+bit.bounce(t,4.1,.35,.08)
    bit.armR.rotation_euler.x=bit.armL.rotation_euler.x=-2.8*seg(t,3.6,3.75)*(1-seg(t,4.6,4.9))
    bit.armR.rotation_euler.x+=-2.0*seg(t,20.4,20.6)
    bit.R.rotation_euler.z=math.radians(-35)*seg(t,20.2,20.5); bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(3.6<t<5 or t>20.3))
    bit.tip.hide_render=(3.6<t<4.8 and int(t*12)%2==0)
    # Clawd explains, pointing at the monitor
    clawd.R.rotation_euler.z=math.radians(-20)*seg(t,3.7,4.0)*(1-seg(t,5.0,5.3)) + math.radians(30)*seg(t,10.4,10.8)*(1-seg(t,16.9,17.2))
    clawd.armR.rotation_euler.x=-2.4*seg(t,10.5,10.7)*(1-seg(t,16.8,17.1)) - 1.4*seg(t,5.3,5.5)*(1-seg(t,7.4,7.6))
    clawd.B.location.z=clawd.bounce(t,15.6,.35,.07)
    clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t>20.6))
    fl=.35*seg(t,21.4,21.6)*(.5+.5*(int(t*9)%3!=0)) if t>21.4 else 0; red_alert(fl)
render_loop(animate)
