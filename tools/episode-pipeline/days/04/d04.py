# ----- Day 4: The Prompt Formula -----
clawd=Toon("clawd",(.3,-.3,0),ORA)
bit=Toon("bit",(-.25,-.25,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
GR=mat("printer",(.12,.12,.13),.5)
boxo("printer",(-.68,.2,.1),(.42,.32,.2),GR,.01); boxo("ptray",(-.68,.0,.17),(.3,.12,.01),mat("pwhite",(.9,.9,.88),.6))
BL=[("ROLE",(.85,.15,.08)),("CONTEXT",(.95,.65,.05)),("TASK",(.05,.75,.7)),("FORMAT",(.55,.25,.9))]
blocks=[]
for i,(nm,col) in enumerate(BL):
    R_=rig("blk"+nm,(0,-.5,0)); v=.03
    part("bk"+nm,vox_box(-.15,.15,-.09,.09,0,.15,v),mat("bk"+nm,col,.45),R_)
    t3=text3d(nm,(0,-.095,.05),size=.06 if len(nm)<6 else .05); t3.parent=R_; t3.location=(0,-.095,.05)
    blocks.append((R_,6.25+i*.55,.155*i))
PR=screen_seq("p",25)
SHOTS=[(0,2.2,(-.3,-1.4,.35),(-.4,-1.1,.3),(-.55,.05,.15),(-.45,-.1,.15),50),
 (2.2,6.1,(.0,-1.9,.35),(.05,-1.6,.33),(.02,-.27,.15),(.02,-.27,.15),50),
 (6.1,8.6,(-.6,-2.1,.55),(.4,-2.1,.5),(0,-.5,.33),(0,-.5,.3),45),
 (8.6,14.1,(.3,-1.9,.45),(.4,-1.4,.5),(.55,.7,.5),(.55,.72,.5),45),
 (14.1,15.9,(-.2,-1.0,.2),(-.22,-.85,.18),(-.25,-.25,.12),(-.25,-.25,.12),55),
 (15.9,30,(-.5,-1.2,.25),(-.35,-.95,.2),(-.12,-.27,.13),(-.25,-.25,.12),50)]
def animate(t,FRi):
    a0=camera(t,SHOTS)
    # Bit shoots out of the printer and lands
    kk=eo(seg(t,.05,.75)); p0=Vector((-.68,.2,.22)); p1=Vector((-.25,-.25,0))
    bp=p0.lerp(p1,kk); bp.z+=math.sin(min(1,seg(t,.05,.75))*math.pi)*.35; bit.R.location=bp
    bit.R.rotation_euler.z=(1-kk)*6.28*1.5 + math.radians(20)*seg(t,2.2,2.6)*(1-seg(t,15.8,16.2))
    sq=.12*math.exp(-max(0,t-.75)*9)*(t>.75); bit.B.scale=(1+sq,1,1-sq)
    bit.B.location.z=bit.bounce(t,14.25,.35,.09)+bit.bounce(t,14.6,.35,.06)+(abs(math.sin(t*14))*.006 if t<1.9 else 0)
    bit.armR.rotation_euler.x=-2.4*seg(t,.4,.6)*(1-seg(t,1.6,1.8)) - (2.2+.4*math.sin(t*16))*(14.2<t<15.2)
    bit.armL.rotation_euler.x=-(2.2+.4*math.sin(t*16+1))*(14.2<t<15.2)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(t<1.0 or 16<t<16.6)); bit.tip.hide_render=(t>16.2 and int(t*8)%2==0)
    if t>15.9: bit.R.location.x=-.25+.06*ease(seg(t,15.9,16.5))   # leans in to whisper
    # Clawd: startled, turns to Bit, teaches, points at the blocks / monitor
    clawd.R.rotation_euler.z=math.radians(-25)*seg(t,1.0,1.4)*(1-seg(t,6.0,6.3)) + math.radians(30)*seg(t,8.7,9.1)*(1-seg(t,13.9,14.2)) + math.radians(-30)*seg(t,15.9,16.3)
    clawd.B.location.z=clawd.bounce(t,.35,.35,.12)
    clawd.armL.rotation_euler.x=-2.0*seg(t,6.2,6.35)*(1-seg(t,8.3,8.6))
    clawd.armR.rotation_euler.x=-2.3*seg(t,8.9,9.1)*(1-seg(t,13.7,14.0))
    clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(.35<t<1.3 or t>17.2))
    # blocks drop in and stack
    for R_,t0,z in blocks:
        k2=seg(t,t0,t0+.3); gone=seg(t,8.55,8.85); R_.location.z=z+(1-eo(k2))*.9+gone*1.5; hid=t<t0 or gone>=1; R_.hide_render=hid
        for ch in R_.children: ch.hide_render=hid
        R_.rotation_euler.z=(1-eo(k2))*.6
    # monitor
    im.image=PR[int(seg(t,8.9,13.6)*24)] if t>8.85 else bpy.data.images["screen.png"]
    # red flicker at the end
    fl=seg(t,17.0,17.3)*(.55+.45*(int(t*11)%3!=0)) if t>17.0 else 0; red_alert(fl)
render_loop(animate)
