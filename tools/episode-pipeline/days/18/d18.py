# generated for day 18
clawd=Toon("clawd",(0.3,-0.3,0),ORA)
bit=Toon("bit",(-0.15,-0.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,0.3,-.15))
REDE2=mat("infred",(1,.03,.03),.3,em=18,emc=(1,.03,.03)); V_=clawd.V; DD_=9; W_=13
rEyes=part("cInfEyes",[((x*V_,-DD_*V_/2-V_*.34,(3+9*.47)*V_),(V_*.95,V_*.6,V_*1.9)) for x in (-3,3)],REDE2,clawd.B,(0,-DD_*V_/2,(3+9*.47)*V_)); rEyes.hide_render=True
CMAT=bpy.data.materials["clawdm"]
SCR={}
SCR["ch"]=screen_seq("ch",3)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 1.9, (-0.18, -0.95, 0.2), (-0.2, -0.82, 0.18), (-0.22, -0.25, 0.12), (-0.22, -0.25, 0.12), 55), (1.9, 5.4, (0.0, -1.0, 0.25), (-0.02, -0.85, 0.22), (0.25, -0.3, 0.14), (0.25, -0.3, 0.14), 50), (5.4, 8.0, (0.0, -1.0, 0.25), (-0.02, -0.85, 0.22), (0.25, -0.3, 0.14), (0.25, -0.3, 0.14), 50), (8.0, 15.3, (0.4, -1.8, 0.5), (0.5, -1.3, 0.52), (0.55, 0.72, 0.5), (0.55, 0.72, 0.5), 45), (15.3, 17.0, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (17.0, 40, (0.0, -1.0, 0.25), (-0.02, -0.85, 0.22), (0.25, -0.3, 0.14), (0.25, -0.3, 0.14), 50)]
TM_ENV=ENV
def speak(who,FRi):
    e=ENV.get(who,[]); lo=max(0,FRi-6); hi=min(len(e),FRi+7)
    return 1.0 if (hi>lo and max(e[lo:hi])>.2) else 0.0
def smooth(who,t):
    return speak(who,int(t*24))

PROPS=[]
def dim(l):
    for L_,(e0,c0) in zip(LIGHTS,LBASE): L_.data.energy=e0*(1-.93*l)
    bpy.data.worlds[0].node_tree.nodes["Background"].inputs["Color"].default_value=(.015*(1-l),.012*(1-l),.01*(1-l),1)

def animate(t,FRi):
    camera(t,SHOTS)
    img=NORMAL
    if t>=8.0: img=SCR["ch"][0]
    if t>=12.0: img=SCR["ch"][1]
    if t>=20.9: img=SCR["ch"][2]
    im.image=img
    if 1.5<=t<20.6: red_alert(0.35*(.7+.3*(int(t*8)%2)))
    dk=0
    dk=max(dk,seg(t,20.8,21.2)*(1-seg(t,25.35,25.75)))
    dim(dk)
    sp=smooth('clawd',t)
    clawd.talk('clawd',FRi)
    clawd.B.location.z=clawd.bounce(t,99,.35,.1)*0+abs(math.sin(t*14))*.012*sp
    clawd.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9
    clawd.eyes_set(t,1.3,wide=False)
    sp=smooth('bit',t)
    bit.talk('bit',FRi)
    bit.B.location.z=bit.bounce(t,99,.35,.1)*0+abs(math.sin(t*14))*.012*sp
    bit.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9
    bit.eyes_set(t,0.7,wide=False)
    sp=smooth('maya',t); maya.talk('maya',FRi); maya.armR.rotation_euler.x=(-1.2-.3*math.sin(t*5))*sp; maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.H.rotation_euler.z=.05*math.sin(t*2); maya.eyes.scale.z=.12 if blink(t,.4) else 1
    clawd.R.location.x+=math.sin(t*60)*.006*seg(t,1.9,2.15)*(1-seg(t,4.75,5.0))
    maya.armL.rotation_euler.x+=-2.6*seg(t,15.4,15.65)*(1-seg(t,16.25,16.5)); maya.armR.rotation_euler.x+=-2.6*seg(t,15.4,15.65)*(1-seg(t,16.25,16.5))
    bit.eyes.scale.z=1.5 if 0.3<=t<1.9 else bit.eyes.scale.z
    inf=(seg(t,1.5,1.8)*(1-seg(t,16.5,16.8)))*(1 if int(t*10)%3 else .3)
    rEyes.hide_render=(inf<.5); clawd.eyes.hide_render=(inf>=.5)
    cc=[ORA[i]*(1-inf)+(.9,.02,.02)[i]*inf for i in range(3)]; CMAT.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*cc,1)
    bk=seg(t,19.3,20.1); cc=[ORA[i]*(1-bk)+(.01,.01,.01)[i]*bk for i in range(3)]; CMAT.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*cc,1)
render_loop(animate)
