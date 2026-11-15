# generated for day 29
clawd=Toon("clawd",(0.3,-0.3,0),ORA)
CMAT=bpy.data.materials["clawdm"]
bit=Toon("bit",(-0.15,-0.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
REDE=mat("nullred",(1,.03,.03),.3,em=16,emc=(1,.03,.03))
null=Toon("null",(0.7,-0.25,0),(.015,.012,.015),scale=.6,eyem=REDE)
maya=Human("maya",(1.5,0.3,-.15))
SCR={}
SCR["tl"]=screen_seq("tl",1)
SCR["md"]=screen_seq("md",2)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 2.5, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (2.5, 9.0, (0.55, -2.5, 0.62), (0.55, -2.1, 0.6), (0.55, 0, 0.4), (0.55, -0.2, 0.35), 38), (9.0, 17.2, (0.4, -1.8, 0.5), (0.5, -1.3, 0.52), (0.55, 0.72, 0.5), (0.55, 0.72, 0.5), 45), (17.2, 40, (0.5, -1.5, 0.5), (0.56, -0.85, 0.52), (0.55, 0.72, 0.52), (0.55, 0.72, 0.52), 50)]
TM_ENV=ENV
def speak(who,FRi):
    e=ENV.get(who,[]); lo=max(0,FRi-6); hi=min(len(e),FRi+7)
    return 1.0 if (hi>lo and max(e[lo:hi])>.2) else 0.0
def smooth(who,t):
    return speak(who,int(t*24))

PROPS=[]
R_=random.Random(5); CONF=[]
for i in range(90):
    col=[(.9,.1,.1),(.1,.5,.95),(.95,.75,.1),(.2,.8,.4),(.8,.3,.8),(1,.5,.1)][i%6]
    o=boxo("cf%d"%i,(0,0,0),(.03,.03,.03),mat("cf%d"%i,col,.4)); CONF.append((o,Vector((R_.uniform(-.9,.9),R_.uniform(.0,1.0),R_.uniform(1.2,2.2))),Vector((R_.uniform(-6,6),R_.uniform(-6,6),R_.uniform(-6,6)))))
def dim(l):
    for L_,(e0,c0) in zip(LIGHTS,LBASE): L_.data.energy=e0*(1-.93*l)
    bpy.data.worlds[0].node_tree.nodes["Background"].inputs["Color"].default_value=(.015*(1-l),.012*(1-l),.01*(1-l),1)

def animate(t,FRi):
    camera(t,SHOTS)
    img=NORMAL
    if t>=9.3: img=SCR["tl"][0]
    if t>=17.3: img=SCR["md"][0]
    im.image=img
    if 17.3<=t<22.26: red_alert(0.6*(.7+.3*(int(t*8)%2)))
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
    maya.armL.rotation_euler.x+=-2.6*seg(t,0.3,0.55)*(1-seg(t,2.15,2.4)); maya.armR.rotation_euler.x+=-2.6*seg(t,0.3,0.55)*(1-seg(t,2.15,2.4))
    bit.B.location.z+=abs(math.sin(seg(t,2.5,5.8)*math.pi*4))*0.1
    clawd.B.location.z+=abs(math.sin(seg(t,2.5,6.0)*math.pi*3))*0.1
    pu=seg(t,0,1.2); NM=bpy.data.materials['nullm'].node_tree.nodes['Principled BSDF'].inputs['Base Color']; NM.default_value=(.015+.5*pu,.012+.1*pu,.015+.8*pu,1); REDE.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(1-.5*pu,.03+.1*pu,.03+.9*pu,1)
    for o,v0,rt in CONF:
        tt=max(0,t-2.5); o.hide_render=t<2.5; o.location=Vector((.55,.6,.5))+Vector((v0.x*tt*.9,v0.y*tt*.4,v0.z*tt*.6-1.6*tt*tt)); o.rotation_euler=rt*tt
render_loop(animate)
