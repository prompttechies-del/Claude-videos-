# ----- Day 16: The Deck -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.15,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
DK=screen_seq("dk",3); OL=screen_seq("ol",25)
SHOTS=[(0,3.1,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (3.1,5.9,(.0,-1.5,.33),(.05,-1.25,.32),(.2,-.3,.15),(.2,-.3,.15),42),
 (5.9,17.0,(.4,-1.8,.5),(.52,-1.3,.52),(.55,.72,.5),(.55,.72,.5),45),
 (17.0,20.5,(1.75,-1.9,.75),(1.55,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (20.5,40,(.55,-1.5,.5),(.55,-.85,.52),(.55,.72,.52),(.55,.72,.52),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    if t<6.2: im.image=DK[0]
    elif t<12.4: im.image=OL[int(seg(t,6.3,12.2)*24)]
    elif t<20.6: im.image=DK[1]
    else: im.image=DK[2]
    red_alert(.5*seg(t,20.8,21.2)*(.7+.3*(int(t*7)%2)))
    # Maya at 2 AM: head down, sobbing, then looks up
    down=seg(t,.2,.7)*(1-seg(t,3.0,3.4))*(1-seg(t,17.0,17.3))
    maya.H.rotation_euler.x=.5*down+.05*math.sin(t*2); maya.R.location.z=-.15+.03*math.sin(t*1.3)+(abs(math.sin(t*9))*.015*down)
    maya.armR.rotation_euler.x=-1.9*seg(t,.4,.7)*(1-seg(t,2.9,3.2)) - 1.4*seg(t,17.2,17.5)*(1-seg(t,19.5,19.8))
    maya.talk("maya",FRi); maya.eyes.scale.z=.12 if (blink(t,.4) or down>.5) else 1
    clawd.R.rotation_euler.z=math.radians(-25)*seg(t,3.2,3.6)*(1-seg(t,5.8,6.1))+math.radians(30)*seg(t,6.0,6.4)*(1-seg(t,16.7,17.0))+math.radians(-25)*seg(t,20.7,21.1)
    clawd.armR.rotation_euler.x=-2.3*seg(t,3.3,3.5)*(1-seg(t,5.4,5.7)) - 2.2*seg(t,6.2,6.4)*(1-seg(t,16.4,16.7))
    clawd.B.location.z=clawd.bounce(t,3.3,.35,.1); clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t>21.0))
    bit.armR.rotation_euler.x=-2.4*seg(t,20.9,21.1); bit.R.rotation_euler.z=math.radians(30)*seg(t,20.6,20.9)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t>20.7)); bit.B.location.z=abs(math.sin(t*28))*.004*(t>21)
render_loop(animate)
