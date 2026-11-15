# generated for day 30
clawd=Toon("clawd",(0.3,-0.3,0),ORA)
CMAT=bpy.data.materials["clawdm"]
bit=Toon("bit",(-0.15,-0.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
REDE=mat("nullred",(1,.03,.03),.3,em=16,emc=(1,.03,.03))
null=Toon("null",(0.7,-0.25,0),(.015,.012,.015),scale=.6,eyem=REDE)
maya=Human("maya",(1.5,0.3,-.15))
SCR={}
SCR["rl"]=screen_seq("rl",41)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 4.6, (0.5, -1.4, 0.3), (0.55, -1.15, 0.3), (0.7, -0.2, 0.2), (0.7, -0.2, 0.2), 45), (4.6, 7.0, (0.1, -1.9, 0.4), (0.15, -1.6, 0.38), (0.1, -0.3, 0.2), (0.1, -0.3, 0.2), 45), (7.0, 15.3, (0.4, -1.8, 0.5), (0.5, -1.3, 0.52), (0.55, 0.72, 0.5), (0.55, 0.72, 0.5), 45), (15.3, 17.2, (0.55, -2.5, 0.62), (0.55, -2.1, 0.6), (0.55, 0, 0.4), (0.55, -0.2, 0.35), 38), (17.2, 40, (0.55, -2.5, 0.62), (0.55, -2.1, 0.6), (0.55, 0, 0.4), (0.55, -0.2, 0.35), 38)]
TM_ENV=ENV
def speak(who,FRi):
    e=ENV.get(who,[]); lo=max(0,FRi-6); hi=min(len(e),FRi+7)
    return 1.0 if (hi>lo and max(e[lo:hi])>.2) else 0.0
def smooth(who,t):
    return speak(who,int(t*24))

PROPS=[]
bpy.ops.mesh.primitive_plane_add(size=1,location=(0,0,0)); dr=bpy.context.object; dr.scale=(.9,1.6,1)
DRH=rig("doorH",(-.45,1.55,.0)); dm=boxo("door",(.45,0,.8),(.9,.04,1.6),mat("doorm",(.2,.12,.08),.5)); dm.parent=DRH
bpy.ops.object.light_add(type='AREA',location=(0,1.2,.8)); DL=bpy.context.object; DL.data.energy=0; DL.data.size=2; DL.data.color=(1,.95,.85); DL.rotation_euler=(math.radians(90),0,0)
dr.location=(0,1.57,.8); dr.rotation_euler=(math.pi/2,0,0); dr.data.materials.append(mat("doorlight",(1,.97,.9),.2,em=0,emc=(1,.97,.9))); DLM=dr.data.materials[0]; DLM.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value=(1,.97,.9,1)
def dim(l):
    for L_,(e0,c0) in zip(LIGHTS,LBASE): L_.data.energy=e0*(1-.93*l)
    bpy.data.worlds[0].node_tree.nodes["Background"].inputs["Color"].default_value=(.015*(1-l),.012*(1-l),.01*(1-l),1)

def animate(t,FRi):
    camera(t,SHOTS)
    img=NORMAL
    if t>=7.1: img=SCR["rl"][min(len(SCR["rl"])-1,int(seg(t,7.6,15.0)*(len(SCR["rl"])-1)))]
    im.image=img
    if 0.2<=t<17.3: red_alert(0.5*(.7+.3*(int(t*8)%2)))
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
    clawd.R.location.x+=0.35*ease(seg(t,4.7,5.5))*(1-ease(seg(t,5.7,6.5)))
    maya.armL.rotation_euler.x+=-2.6*seg(t,17.3,17.55)*(1-seg(t,19.75,20)); maya.armR.rotation_euler.x+=-2.6*seg(t,17.3,17.55)*(1-seg(t,19.75,20))
    pu=seg(t,0,1.2); NM=bpy.data.materials['nullm'].node_tree.nodes['Principled BSDF'].inputs['Base Color']; NM.default_value=(.015+.5*pu,.012+.1*pu,.015+.8*pu,1); REDE.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(1-.5*pu,.03+.1*pu,.03+.9*pu,1)
    DRH.rotation_euler.z=-1.5*eo(seg(t,17.3,17.8)); DL.data.energy=900*seg(t,17.3,17.8); DLM.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value=40*seg(t,17.3,17.8)
render_loop(animate)
