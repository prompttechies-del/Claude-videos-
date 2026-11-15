# ----- Day 15: The Research -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.15,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
PAP=mat("paper2",(.92,.9,.86),.6); R_=random.Random(9); sheets=[]
for i in range(26):
    o=boxo("sh%d"%i,(0,0,0),(.21,.297,.003),PAP); p=Vector((-.62+R_.uniform(-.05,.05),-.15+R_.uniform(-.05,.05),.003+i*.007))
    o.location=p; o.rotation_euler.z=R_.uniform(-.3,.3); sheets.append((o,p,R_.uniform(0,6.28),R_.uniform(.25,.5),i))
brief=boxo("brief",(0,0,0),(.21,.297,.004),mat("briefm",(.98,.97,.92),.5)); bt=text3d("BRIEF",(0,0,.004),size=.06,col=(.1,.2,.6),em=.5,rot=(0,0,0)); bt.parent=brief
BR=screen_seq("br",8)
SHOTS=[(0,3.7,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (3.7,5.75,(-.35,-1.3,.5),(-.45,-1.05,.45),(-.6,-.15,.12),(-.6,-.15,.12),42),
 (5.75,16.2,(.4,-1.8,.5),(.5,-1.3,.52),(.55,.72,.5),(.55,.72,.5),45),
 (16.2,40,(.85,-.9,.32),(.75,-.2,.3),(.72,.72,.29),(.72,.72,.29),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    n=0 if t<9.0 else min(5,1+int((t-9.0)/.55)); n=6 if t>12.4 else n; n=7 if t>16.6 else n
    im.image=BR[n] if t>6.0 else bpy.data.images["screen.png"]
    # the pile swirls into one brief
    for o,p,a,r,i in sheets:
        k=seg(t,4.0+i*.02,5.0+i*.02); ang=a+k*7; c=Vector((-.6,-.15,.25))
        sw=c+Vector((math.cos(ang)*r*(1-k),math.sin(ang)*r*(1-k)*.6,math.sin(k*math.pi)*.25))
        o.location=p.lerp(sw,math.sin(min(k,1)*math.pi/2)) if k<1 else c; o.hide_render=k>=1
        o.rotation_euler=(k*3,k*2,o.rotation_euler.z if k==0 else ang)
    kb=eo(seg(t,5.0,5.5)); brief.location=Vector((-.6,-.15,.25)).lerp(Vector((-.6,-.2,.004)),kb); brief.hide_render=t<4.95; bt.hide_render=t<4.95
    brief.rotation_euler.z=(1-kb)*3
    red_alert(.5*seg(t,16.7,17.1)*(.7+.3*(int(t*7)%2)))
    maya.armL.rotation_euler.x=maya.armR.rotation_euler.x=-1.4*seg(t,.5,.8)*(1-seg(t,3.2,3.5))
    maya.H.rotation_euler.x=.15*seg(t,1,1.5)*(1-seg(t,3,3.4)); maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else (1.4 if t>16.8 else 1)
    clawd.armR.rotation_euler.x=-2.4*seg(t,3.9,4.1)*(1-seg(t,5.3,5.6)) - 2.2*seg(t,6.0,6.2)*(1-seg(t,15.4,15.7))
    clawd.R.rotation_euler.z=math.radians(-30)*seg(t,3.8,4.1)*(1-seg(t,5.6,5.9))+math.radians(30)*seg(t,5.9,6.3)*(1-seg(t,15.8,16.1))
    clawd.B.location.z=clawd.bounce(t,4.0,.35,.1); clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t>16.8))
    bit.armR.rotation_euler.x=-2.4*seg(t,16.5,16.7); bit.R.rotation_euler.z=math.radians(30)*seg(t,16.3,16.6)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t>16.4))
render_loop(animate)
