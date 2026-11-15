# ----- Day 10: Phishing Bait -----
clawd=Toon("clawd",(-.45,-.3,0),ORA)
bit=Toon("bit",(.25,.1,.035),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
ML=screen_seq("ml",3); DL=screen_seq("dl",26)
SHOTS=[(0,2.15,(.25,-1.0,.3),(.22,-.8,.28),(.25,.3,.2),(.25,.1,.08),45),
 (2.15,3.3,(-.1,-1.6,.35),(.0,-1.4,.33),(0,0,.12),(0,-.05,.1),38),
 (3.3,10.3,(.4,-1.8,.5),(.5,-1.3,.52),(.55,.72,.5),(.55,.72,.5),45),
 (10.3,15.3,(.0,-1.5,.33),(.05,-1.25,.32),(-.05,-.2,.15),(-.05,-.2,.12),42),
 (15.3,17.1,(-.18,-.95,.2),(-.2,-.82,.18),(-.22,-.25,.12),(-.22,-.25,.12),55),
 (17.1,40,(.55,-1.4,.5),(.55,-.85,.52),(.55,.72,.52),(.55,.72,.52),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    im.image=DL[int(seg(t,17.2,19.0)*25)] if t>17.1 else ML[(t>3.9)+(t>10.6)]
    # Bit hops on the keyboard about to click; gets tackled
    tk=seg(t,2.3,2.75); land=eo(seg(t,2.6,3.2))
    bp=Vector((.25,.1,.035)).lerp(Vector((-.22,-.25,0)),land); bp.z+=math.sin(seg(t,2.6,3.2)*math.pi)*.18
    bit.R.location=bp; bit.R.rotation_euler.y=-6.28*eo(seg(t,2.6,3.2))
    bit.B.location.z=(abs(math.sin(t*9))*.05 if t<2.2 else 0); bit.armR.rotation_euler.x=-2.6*seg(t,.4,.6)*(1-seg(t,2.4,2.6)) - 1.0*seg(t,15.5,15.8)
    bit.R.rotation_euler.z=math.radians(-20)*seg(t,3.3,3.6)*(1-seg(t,15.3,15.6)) + math.radians(-15)*seg(t,15.6,16)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t<3.4 or t>17.2),shut=(15.8<t<16.3))
    # Clawd dives
    cp=Vector((-.45,-.3,0)).lerp(Vector((.12,0,0)),eo(tk)).lerp(Vector((.12,-.3,0)),ease(seg(t,3.0,3.6))); cp.z=math.sin(tk*math.pi)*.2
    clawd.R.location=cp; clawd.R.rotation_euler.y=.6*math.sin(tk*math.pi)
    clawd.R.rotation_euler.z=math.radians(25)*seg(t,3.6,4)*(1-seg(t,10.1,10.4)) + math.radians(-30)*seg(t,15.5,15.9)
    clawd.armR.rotation_euler.x=clawd.armL.rotation_euler.x=-2.8*seg(t,2.2,2.35)*(1-seg(t,2.9,3.1))
    clawd.armR.rotation_euler.x+=-2.3*seg(t,3.7,3.9)*(1-seg(t,9.9,10.2)); clawd.armL.rotation_euler.x+=-1.5*seg(t,10.6,10.8)*(1-seg(t,14.6,14.9))
    clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(2.1<t<3.3 or t>17.2))
    red_alert(.5*seg(t,18.8,19.1)*(.7+.3*(int(t*9)%2)))
render_loop(animate)
