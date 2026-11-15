# generated for day 19
clawd=Toon("clawd",(0.3,-0.3,0),ORA)
CMAT=bpy.data.materials["clawdm"]
bit=Toon("bit",(-0.15,-0.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
SCR={}
SCR["nt"]=screen_seq("nt",1)
SCR["sc"]=screen_seq("sc",25)
SCR["or"]=screen_seq("or",13)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 2.6, (-0.18, -0.95, 0.2), (-0.2, -0.82, 0.18), (-0.22, -0.25, 0.12), (-0.22, -0.25, 0.12), 55), (2.6, 8.0, (0.4, -1.8, 0.5), (0.5, -1.3, 0.52), (0.55, 0.72, 0.5), (0.55, 0.72, 0.5), 45), (8.0, 12.6, (0.5, -1.5, 0.5), (0.56, -0.85, 0.52), (0.55, 0.72, 0.52), (0.55, 0.72, 0.52), 50), (12.6, 17.0, (-0.18, -0.95, 0.2), (-0.2, -0.82, 0.18), (-0.22, -0.25, 0.12), (-0.22, -0.25, 0.12), 55), (17.0, 40, (0.5, -1.5, 0.5), (0.56, -0.85, 0.52), (0.55, 0.72, 0.52), (0.55, 0.72, 0.52), 50)]
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
    if t>=4.6: img=SCR["nt"][0]
    if t>=7.9: img=SCR["sc"][min(len(SCR["sc"])-1,int(seg(t,8.2,11.5)*(len(SCR["sc"])-1)))]
    if t>=13.2: img=SCR["or"][min(len(SCR["or"])-1,int(seg(t,13.3,15.5)*(len(SCR["or"])-1)))]
    im.image=img
    red_alert(0)
    dk=0
    dk=max(dk,seg(t,0.0,0.4)*(1-seg(t,12.6,13.0)))
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
    bit.R.location.x+=math.sin(t*60)*.006*seg(t,0.5,0.75)*(1-seg(t,2.25,2.5))
    bit.B.location.z+=abs(math.sin(seg(t,10.4,12.4)*math.pi*2))*0.1
    bk=seg(t,0.0,0.8); cc=[ORA[i]*(1-bk)+(.01,.01,.01)[i]*bk for i in range(3)]; CMAT.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*cc,1)
render_loop(animate)
