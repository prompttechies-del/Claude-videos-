# ----- Day 13: Proof -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.15,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
PB=screen_seq("pb",1); CMP=screen_seq("cmp",3); NM=screen_seq("nm",25)
SHOTS=[(0,2.4,(-.12,-1.0,.22),(-.14,-.85,.2),(-.15,-.3,.12),(-.15,-.3,.12),50),
 (2.4,5.0,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (5.0,7.6,(.35,-1.6,.4),(.4,-1.3,.42),(.45,.3,.35),(.3,-.3,.15),45),
 (7.6,9.15,(1.15,-2.3,.6),(1.05,-2.0,.58),(1.1,.0,.42),(1.3,.1,.5),32),
 (9.15,16.4,(.4,-1.8,.5),(.5,-1.3,.52),(.55,.72,.5),(.55,.72,.5),45),
 (16.4,40,(.55,-1.4,.5),(.55,-.85,.52),(.55,.72,.52),(.55,.72,.52),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    if t<5.1: im.image=bpy.data.images["screen.png"]
    elif t<9.2: im.image=PB[0]
    elif t<16.5: im.image=CMP[(t>12.0)+(t>14.6)]
    else: im.image=NM[int(seg(t,16.6,19.4)*24)]
    red_alert(.5*seg(t,16.5,16.9)*(.7+.3*(int(t*7)%2)))
    bit.B.location.z=abs(math.sin(t*9))*.04*(t<2.2)+bit.bounce(t,7.8,.35,.12); bit.armR.rotation_euler.x=-2.4*seg(t,.4,.6)*(1-seg(t,2.0,2.3))
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t>16.6))
    clawd.R.rotation_euler.z=math.radians(-25)*seg(t,2.5,2.8)*(1-seg(t,9.0,9.3))+math.radians(30)*seg(t,9.4,9.8)*(1-seg(t,15.6,16))
    clawd.armR.rotation_euler.x=-2.3*seg(t,5.3,5.5)*(1-seg(t,7.2,7.5)) - 2.2*seg(t,9.6,9.8)*(1-seg(t,15.4,15.7))
    clawd.B.location.z=clawd.bounce(t,7.8,.35,.1); clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t>16.6))
    maya.armL.rotation_euler.x=maya.armR.rotation_euler.x=-2.6*seg(t,7.8,8.0)*(1-seg(t,8.9,9.2))
    maya.H.rotation_euler.z=math.radians(-28)*seg(t,2.5,2.8)+.05*math.sin(t*2); maya.R.location.z=-.15+.03*math.sin(t*1.3)+abs(math.sin(t*10))*.03*(7.8<t<8.9)
    maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else (1.4 if t>16.6 else 1)
render_loop(animate)
