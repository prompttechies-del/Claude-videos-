# generated for day 22
bit=Toon("bit",(-0.15,-0.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,0.3,-.15))
SCR={}
SCR["vc"]=screen_seq("vc",3)
SCR["fm"]=screen_seq("fm",25)
NORMAL=bpy.data.images['screen.png']
SHOTS=[(0, 4.2, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (4.2, 7.0, (0.5, -1.5, 0.5), (0.56, -0.85, 0.52), (0.55, 0.72, 0.52), (0.55, 0.72, 0.52), 50), (7.0, 13.2, (1.75, -1.9, 0.75), (1.62, -1.6, 0.72), (1.5, 0.3, 0.68), (1.5, 0.2, 0.7), 50), (13.2, 18.3, (0.4, -1.8, 0.5), (0.5, -1.3, 0.52), (0.55, 0.72, 0.5), (0.55, 0.72, 0.5), 45), (18.3, 21.4, (0.5, -1.5, 0.5), (0.56, -0.85, 0.52), (0.55, 0.72, 0.52), (0.55, 0.72, 0.52), 50), (21.4, 40, (-0.18, -0.95, 0.2), (-0.2, -0.82, 0.18), (-0.22, -0.25, 0.12), (-0.22, -0.25, 0.12), 55)]
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
    if t>=0: lv_=env("vance",FRi); img=SCR["vc"][0 if lv_<.18 else (1 if lv_<.55 else 2)]
    if t>=13.4: img=SCR["fm"][min(len(SCR["fm"])-1,int(seg(t,13.8,17.8)*(len(SCR["fm"])-1)))]
    if t>=18.2: lv_=env("vance",FRi); img=SCR["vc"][0 if lv_<.18 else (1 if lv_<.55 else 2)]
    im.image=img
    if 21.6<=t<26.18: red_alert(0.35*(.7+.3*(int(t*8)%2)))
    dk=0
    sp=smooth('bit',t)
    bit.talk('bit',FRi)
    bit.B.location.z=bit.bounce(t,99,.35,.1)*0+abs(math.sin(t*14))*.012*sp
    bit.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9
    bit.eyes_set(t,0.7,wide=False)
    sp=smooth('maya',t); maya.talk('maya',FRi); maya.armR.rotation_euler.x=(-1.2-.3*math.sin(t*5))*sp; maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.H.rotation_euler.z=.05*math.sin(t*2); maya.eyes.scale.z=.12 if blink(t,.4) else 1
    maya.R.rotation_euler.x+=0.1*seg(t,0.4,0.65)*(1-seg(t,3.55,3.8))
    bit.R.location.x+=math.sin(t*60)*.006*seg(t,21.6,21.85)*(1-seg(t,23.25,23.5))
    bit.eyes.scale.z=1.5 if 21.6<=t<23.5 else bit.eyes.scale.z
render_loop(animate)
