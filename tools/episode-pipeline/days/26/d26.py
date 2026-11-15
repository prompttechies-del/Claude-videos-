# generated for day 26
clawd=Toon("clawd",(0.15,-0.3,0),ORA)
CMAT=bpy.data.materials["clawdm"]
bit=Toon("bit",(-0.15,-0.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
REDE=mat("nullred",(1,.03,.03),.3,em=16,emc=(1,.03,.03))
null=Toon("null",(0.7,-0.25,0),(.015,.012,.015),scale=.6,eyem=REDE)
maya=Human("maya",(1.5,0.3,-.15))
SCR={}
SCR["vh"]=screen_seq("vh",1)
SCR["rs"]=screen_seq("rs",13)
SCR["ms"]=screen_seq("ms",25)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 7.0, (0.5, -1.4, 0.3), (0.55, -1.15, 0.3), (0.7, -0.2, 0.2), (0.7, -0.2, 0.2), 45), (7.0, 12.8, (0.5, -1.4, 0.3), (0.55, -1.15, 0.3), (0.7, -0.2, 0.2), (0.7, -0.2, 0.2), 45), (12.8, 21.2, (0.4, -1.8, 0.5), (0.5, -1.3, 0.52), (0.55, 0.72, 0.5), (0.55, 0.72, 0.5), 45), (21.2, 23.3, (0.5, -1.5, 0.5), (0.56, -0.85, 0.52), (0.55, 0.72, 0.52), (0.55, 0.72, 0.52), 50), (23.3, 40, (0.5, -1.5, 0.5), (0.56, -0.85, 0.52), (0.55, 0.72, 0.52), (0.55, 0.72, 0.52), 50)]
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
    if t>=12.9: img=SCR["vh"][0]
    if t>=21.3: img=SCR["rs"][min(len(SCR["rs"])-1,int(seg(t,21.5,23.2)*(len(SCR["rs"])-1)))]
    if t>=23.4: img=SCR["ms"][min(len(SCR["ms"])-1,int(seg(t,23.6,27.5)*(len(SCR["ms"])-1)))]
    im.image=img
    if 23.4<=t<31.43: red_alert(0.5*(.7+.3*(int(t*8)%2)))
    dk=0
    sp=max(smooth('clawd',t),smooth('null',t) if ('clawd'=='clawd' and False) else 0)
    clawd.talk('clawd',FRi)
    clawd.B.location.z=clawd.bounce(t,99,.35,.1)*0+abs(math.sin(t*14))*.012*sp
    clawd.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9
    clawd.eyes_set(t,1.3,wide=False)
    sp=max(smooth('bit',t),smooth('null',t) if ('bit'=='clawd' and False) else 0)
    bit.talk('bit',FRi)
    bit.B.location.z=bit.bounce(t,99,.35,.1)*0+abs(math.sin(t*14))*.012*sp
    bit.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9
    bit.eyes_set(t,0.7,wide=False)
    sp=max(smooth('null',t),smooth('null',t) if ('null'=='clawd' and False) else 0)
    null.talk('null',FRi)
    null.B.location.z=null.bounce(t,99,.35,.1)*0+abs(math.sin(t*14))*.012*sp
    null.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9
    null.eyes_set(t,0.7,wide=False)
    sp=smooth('maya',t); maya.talk('maya',FRi); maya.armR.rotation_euler.x=(-1.2-.3*math.sin(t*5))*sp; maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.H.rotation_euler.z=.05*math.sin(t*2); maya.eyes.scale.z=.12 if blink(t,.4) else 1
    bit.B.location.z+=abs(math.sin(seg(t,21.5,22.6)*math.pi*3))*0.1
    maya.armL.rotation_euler.x+=-2.6*seg(t,0.4,0.65)*(1-seg(t,1.75,2.0)); maya.armR.rotation_euler.x+=-2.6*seg(t,0.4,0.65)*(1-seg(t,1.75,2.0))
    pu=seg(t,2.5,3.7); NM=bpy.data.materials['nullm'].node_tree.nodes['Principled BSDF'].inputs['Base Color']; NM.default_value=(.015+.5*pu,.012+.1*pu,.015+.8*pu,1); REDE.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(1-.5*pu,.03+.1*pu,.03+.9*pu,1)
render_loop(animate)
