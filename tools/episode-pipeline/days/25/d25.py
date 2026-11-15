# generated for day 25
clawd=Toon("clawd",(0.1,-0.3,0),ORA)
CMAT=bpy.data.materials["clawdm"]
bit=Toon("bit",(-0.25,-0.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
REDE=mat("nullred",(1,.03,.03),.3,em=16,emc=(1,.03,.03))
null=Toon("null",(0.7,-0.25,0),(.015,.012,.015),scale=.6,eyem=REDE)
maya=Human("maya",(1.5,0.3,-.15))
SCR={}
SCR["ex"]=screen_seq("ex",2)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 8.0, (0.5, -1.4, 0.3), (0.55, -1.15, 0.3), (0.7, -0.2, 0.2), (0.7, -0.2, 0.2), 45), (8.0, 11.2, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (11.2, 13.7, (0.4, -1.8, 0.5), (0.5, -1.3, 0.52), (0.55, 0.72, 0.5), (0.55, 0.72, 0.5), 45), (13.7, 20.4, (0.5, -1.4, 0.3), (0.55, -1.15, 0.3), (0.7, -0.2, 0.2), (0.7, -0.2, 0.2), 45), (20.4, 23.1, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (23.1, 40, (0.1, -1.9, 0.4), (0.15, -1.6, 0.38), (0.1, -0.3, 0.2), (0.1, -0.3, 0.2), 45)]
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
    if t>=11.1: img=SCR["ex"][0]
    if t>=20.5: img=SCR["ex"][1]
    im.image=img
    if 20.5<=t<29.49: red_alert(0.25*(.7+.3*(int(t*8)%2)))
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
    maya.armL.rotation_euler.x+=-2.6*seg(t,20.7,20.95)*(1-seg(t,22.75,23.0)); maya.armR.rotation_euler.x+=-2.6*seg(t,20.7,20.95)*(1-seg(t,22.75,23.0))
    clawd.B.location.z+=abs(math.sin(seg(t,23.2,26.5)*math.pi*2))*0.1
    bit.B.location.z+=abs(math.sin(seg(t,23.2,26.5)*math.pi*2))*0.1
render_loop(animate)
