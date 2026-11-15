# generated for day 17
clawd=Toon("clawd",(0.3,-0.3,0),ORA)
maya=Human("maya",(1.5,0.3,-.15))
REDE2=mat("infred",(1,.03,.03),.3,em=18,emc=(1,.03,.03)); V_=clawd.V; DD_=9; W_=13
rEyes=part("cInfEyes",[((x*V_,-DD_*V_/2-V_*.34,(3+9*.47)*V_),(V_*.95,V_*.6,V_*1.9)) for x in (-3,3)],REDE2,clawd.B,(0,-DD_*V_/2,(3+9*.47)*V_)); rEyes.hide_render=True
CMAT=bpy.data.materials["clawdm"]
SCR={}
SCR["pr"]=screen_seq("pr",25)
SCR["qq"]=screen_seq("qq",3)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 4.4, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (4.4, 12.4, (0.0, -1.5, 0.33), (0.05, -1.25, 0.32), (0.2, -0.3, 0.15), (0.2, -0.3, 0.15), 42), (12.4, 14.9, (0.0, -1.0, 0.25), (-0.02, -0.85, 0.22), (0.25, -0.3, 0.14), (0.25, -0.3, 0.14), 50), (14.9, 18.0, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (18.0, 20.6, (0.0, -1.5, 0.33), (0.05, -1.25, 0.32), (0.2, -0.3, 0.15), (0.2, -0.3, 0.15), 42), (20.6, 40, (0.0, -1.0, 0.25), (-0.02, -0.85, 0.22), (0.25, -0.3, 0.14), (0.25, -0.3, 0.14), 50)]
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
    if t>=4.6: img=SCR["pr"][min(len(SCR["pr"])-1,int(seg(t,4.8,11.0)*(len(SCR["pr"])-1)))]
    if t>=12.5: img=SCR["qq"][0]
    if t>=18.0: img=SCR["qq"][1]
    if t>=20.6: img=SCR["qq"][2]
    im.image=img
    if 20.7<=t<24.6: red_alert(0.6*(.7+.3*(int(t*8)%2)))
    dk=0
    sp=smooth('clawd',t)
    clawd.talk('clawd',FRi)
    clawd.B.location.z=clawd.bounce(t,99,.35,.1)*0+abs(math.sin(t*14))*.012*sp
    clawd.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9
    clawd.eyes_set(t,1.3,wide=False)
    sp=smooth('maya',t); maya.talk('maya',FRi); maya.armR.rotation_euler.x=(-1.2-.3*math.sin(t*5))*sp; maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.H.rotation_euler.z=.05*math.sin(t*2); maya.eyes.scale.z=.12 if blink(t,.4) else 1
    maya.R.location.x+=math.sin(t*60)*.006*seg(t,1.8,2.05)*(1-seg(t,3.95,4.2))
    maya.R.rotation_euler.x+=0.25*seg(t,0.4,0.65)*(1-seg(t,1.75,2.0))
    inf=(seg(t,20.7,21.0)*(1-seg(t,24.3,24.6)))*(1 if int(t*10)%3 else .3)
    rEyes.hide_render=(inf<.5); clawd.eyes.hide_render=(inf>=.5)
    cc=[ORA[i]*(1-inf)+(.9,.02,.02)[i]*inf for i in range(3)]; CMAT.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*cc,1)
render_loop(animate)
