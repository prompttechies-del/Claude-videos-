# usage: python3 gen_scene.py DAY -> d<DAY>.py + run<DAY>.py from v<DAY>/ep.json
import sys, json
D=sys.argv[1]; C=json.load(open(f"v{D}/ep.json")); TM=json.load(open(f"v{D}/timing.json"))
PRE={"maya":[[1.75,-1.9,.75],[1.62,-1.6,.72],[1.5,.3,.68],[1.5,.2,.7],50],
 "monitor":[[.4,-1.8,.5],[.5,-1.3,.52],[.55,.72,.5],[.55,.72,.5],45],
 "monitor_close":[[.5,-1.5,.5],[.56,-.85,.52],[.55,.72,.52],[.55,.72,.52],50],
 "clawd":[[.0,-1.5,.33],[.05,-1.25,.32],[.2,-.3,.15],[.2,-.3,.15],42],
 "clawd_close":[[.0,-1.0,.25],[-.02,-.85,.22],[.25,-.3,.14],[.25,-.3,.14],50],
 "bit":[[-.18,-.95,.2],[-.2,-.82,.18],[-.22,-.25,.12],[-.22,-.25,.12],55],
 "wide":[[.55,-2.5,.62],[.55,-2.1,.6],[.55,0,.4],[.55,-.2,.35],38],
 "two":[[.1,-1.9,.4],[.15,-1.6,.38],[.1,-.3,.2],[.1,-.3,.2],45],
 "null":[[.5,-1.4,.3],[.55,-1.15,.3],[.7,-.2,.2],[.7,-.2,.2],45],
 "wren":[[-.45,-1.6,.55],[-.42,-1.1,.55],[-.38,1.2,.5],[-.38,1.2,.5],42],
 "wrenroom":[[-.5,-1.8,.55],[-.45,-1.4,.55],[-.5,.15,.5],[-.5,.15,.5],45],
 "alphacam":[[.9,-1.6,.45],[.95,-1.3,.45],[.95,-.2,.35],[.95,-.2,.35],42],
 "low":[[.1,-1.2,.2],[.15,-1.0,.2],[.3,-.3,.12],[.3,-.3,.12],38]}
shots=[]
for a0,a1,name in C["shots"]:
    p=PRE[name]; shots.append((a0,a1,tuple(p[0]),tuple(p[1]),tuple(p[2]),tuple(p[3]),p[4]))
out=[]
w=out.append
w(f"# generated for day {D}")
cast=C["cast"]
if "clawd" in cast:
    w(f'clawd=Toon("clawd",({cast["clawd"][0]},{cast["clawd"][1]},0),ORA)'); w('CMAT=bpy.data.materials["clawdm"]')
if "bit" in cast: w(f'bit=Toon("bit",({cast["bit"][0]},{cast["bit"][1]},0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)')
if "null" in cast:
    w('REDE=mat("nullred",(1,.03,.03),.3,em=16,emc=(1,.03,.03))')
    w(f'null=Toon("null",({cast["null"][0]},{cast["null"][1]},0),(.015,.012,.015),scale=.6,eyem=REDE)')
if "pixel" in cast: w(f'pixel=Toon("pixel",({cast["pixel"][0]},{cast["pixel"][1]},0),(1,.8,.1),scale=.22,eyem=mat("pixeleye",(.1,.1,.1),.3),W=7,D=5,Hh=6)')
if "alpha" in cast:
    w('AEYE=mat("alphaeye",(1,.75,.1),.3,em=14,emc=(1,.75,.1))')
    w(f'alpha=Toon("alpha",({cast["alpha"][0]},{cast["alpha"][1]},0),(.5,.02,.02),scale=.75,eyem=AEYE)')
if "mirror" in cast: w(f'mirror=Human("mirror",({cast["mirror"][0]},{cast["mirror"][1]},-.15),shirt=(.35,.05,.08),hair=(.02,.02,.02),skin=(.7,.45,.35))')
if "maya" in cast: w(f'maya=Human("maya",({cast["maya"][0]},{cast["maya"][1]},-.15))')
if "wren" in cast: w(f'wren=Human("wren",({cast["wren"][0]},{cast["wren"][1]},-.15),shirt=(.9,.9,.92),hair=(.75,.75,.78),skin=(.8,.58,.45))')
if C.get("infect"):
    w('REDE2=mat("infred",(1,.03,.03),.3,em=18,emc=(1,.03,.03)); V_=clawd.V; DD_=9; W_=13')
    w('rEyes=part("cInfEyes",[((x*V_,-DD_*V_/2-V_*.34,(3+9*.47)*V_),(V_*.95,V_*.6,V_*1.9)) for x in (-3,3)],REDE2,clawd.B,(0,-DD_*V_/2,(3+9*.47)*V_)); rEyes.hide_render=True')
    w('CMAT=bpy.data.materials["clawdm"]')
for n,ch in enumerate(C.get("screens",[])):
    pass
w("SCR={}")
for k,(pre,cnt) in C.get("images",{}).items(): w(f'SCR["{k}"]=screen_seq("{pre}",{cnt})')
w("NORMAL=bpy.data.images['screen.png']")
w(f"SHOTS={shots!r}")
w("TM_ENV=ENV")
w('''def speak(who,FRi):
    e=ENV.get(who,[]); lo=max(0,FRi-6); hi=min(len(e),FRi+7)
    return 1.0 if (hi>lo and max(e[lo:hi])>.2) else 0.0
def smooth(who,t):
    return speak(who,int(t*24))
''')
w("PROPS=[]")
if C.get("confetti"):
    w('''R_=random.Random(5); CONF=[]
for i in range(90):
    col=[(.9,.1,.1),(.1,.5,.95),(.95,.75,.1),(.2,.8,.4),(.8,.3,.8),(1,.5,.1)][i%6]
    o=boxo("cf%d"%i,(0,0,0),(.03,.03,.03),mat("cf%d"%i,col,.4)); CONF.append((o,Vector((R_.uniform(-.9,.9),R_.uniform(.0,1.0),R_.uniform(1.2,2.2))),Vector((R_.uniform(-6,6),R_.uniform(-6,6),R_.uniform(-6,6)))))''')
if C.get("door"):
    w('''bpy.ops.mesh.primitive_plane_add(size=1,location=(0,0,0)); dr=bpy.context.object; dr.scale=(.9,1.6,1)
DRH=rig("doorH",(-.45,1.55,.0)); dm=boxo("door",(.45,0,.8),(.9,.04,1.6),mat("doorm",(.2,.12,.08),.5)); dm.parent=DRH
bpy.ops.object.light_add(type='AREA',location=(0,1.2,.8)); DL=bpy.context.object; DL.data.energy=0; DL.data.size=2; DL.data.color=(1,.95,.85); DL.rotation_euler=(math.radians(90),0,0)
dr.location=(0,1.57,.8); dr.rotation_euler=(math.pi/2,0,0); dr.data.materials.append(mat("doorlight",(1,.97,.9),.2,em=0,emc=(1,.97,.9))); DLM=dr.data.materials[0]; DLM.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value=(1,.97,.9,1)''')
w("""def dim(l):
    for L_,(e0,c0) in zip(LIGHTS,LBASE): L_.data.energy=e0*(1-.93*l)
    bpy.data.worlds[0].node_tree.nodes["Background"].inputs["Color"].default_value=(.015*(1-l),.012*(1-l),.01*(1-l),1)
""")
w("def animate(t,FRi):")
w("    camera(t,SHOTS)")
for n in ("clawd","bit","null","pixel","alpha"):
    if n in cast:
        w(f"    {n}.R.rotation_euler=(0,0,0); {n}.R.location.x={cast[n][0]}; {n}.R.location.y={cast[n][1]}; {n}.R.scale=(1,1,1); {n}.B.rotation_euler=(0,0,0); {n}.armL.rotation_euler=(0,0,0); {n}.armR.rotation_euler=(0,0,0)")
if "wren" in cast: w("    wren.R.rotation_euler=(0,0,0); wren.armL.rotation_euler=(0,0,0); wren.armR.rotation_euler=(0,0,0); wren.H.rotation_euler=(0,0,0)")
if "maya" in cast:
    w(f"    maya.R.rotation_euler=(0,0,0); maya.R.location.x={cast['maya'][0]}; maya.armL.rotation_euler=(0,0,0); maya.armR.rotation_euler=(0,0,0); maya.H.rotation_euler=(0,0,0)")
# screens timeline
sc=C.get("screens",[])
if sc:
    w("    img=NORMAL")
    for s in sc:
        t0=s["t"]; key=s["img"]
        if "mouth" in s:
            who=s["mouth"]; w(f'    if t>={t0}: lv_=env("{who}",FRi); img=SCR["{key}"][0 if lv_<.18 else (1 if lv_<.55 else 2)]')
        elif "seq" in s:
            a,b=s["seq"]; w(f'    if t>={t0}: img=SCR["{key}"][min(len(SCR["{key}"])-1,int(seg(t,{a},{b})*(len(SCR["{key}"])-1)))]')
        else: w(f'    if t>={t0}: img=SCR["{key}"][{s.get("idx",0)}]')
    w("    im.image=img")
# alerts and dimming
for a,b,l in C.get("alert",[]): w(f"    if {a}<=t<{b}: red_alert({l}*(.7+.3*(int(t*8)%2)))")
if not C.get("alert"): w("    red_alert(0)")
dk=C.get("dark",[])
w("    dk=0")
for a,b in dk: w(f"    dk=max(dk,seg(t,{a},{a+.4})*(1-seg(t,{b-.4},{b})))")
if dk: w("    dim(dk)")
# characters
def toon(n,spec):
    w(f"    sp=max(smooth('{n}',t),smooth('null',t) if ('{n}'=='clawd' and {bool(C.get('null_in_clawd'))}) else 0)")
    if n=="clawd" and C.get("null_in_clawd"): w("    clawd.talk('clawd',FRi,force=max(env('clawd',FRi),env('null',FRi)))")
    else: w(f"    {n}.talk('{n}',FRi)")
    w(f"    {n}.B.location.z={n}.bounce(t,{spec.get('hop',99)},.35,.1)*0+abs(math.sin(t*14))*.012*sp")
    w(f"    {n}.armR.rotation_euler.x=(-1.3-.5*math.sin(t*6))*sp*.9")
    w(f"    {n}.eyes_set(t,{1.3 if n=='clawd' else .7},wide=False)")
for n in ("clawd","bit","null","pixel","alpha"):
    if n in cast: toon(n,cast[n] if isinstance(cast[n],dict) else {})
if "maya" in cast:
    w("    sp=smooth('maya',t); maya.talk('maya',FRi); maya.armR.rotation_euler.x=(-1.2-.3*math.sin(t*5))*sp; maya.R.location.z=-.15+.03*math.sin(t*1.3)")
    w("    maya.H.rotation_euler.z=.05*math.sin(t*2); maya.eyes.scale.z=.12 if blink(t,.4) else 1")
if "mirror" in cast: w("    sp=smooth('mirror',t); mirror.talk('mirror',FRi); mirror.armR.rotation_euler.x=(-1.1-.3*math.sin(t*5))*sp; mirror.R.location.z=-.15+.02*math.sin(t*1.1); mirror.R.rotation_euler=(0,0,0)")
if "wren" in cast:
    w("    sp=smooth('creator',t); wren.talk('creator',FRi); wren.armR.rotation_euler.x=(-1.1-.3*math.sin(t*5))*sp; wren.R.location.z=-.15+.02*math.sin(t*1.3); wren.eyes.scale.z=.12 if blink(t,.9) else 1")
# events
for ev in C.get("events",[]):
    a,b=ev["t"]; who=ev["who"]; act=ev["act"]; v=ev.get("v",1)
    obj={"maya":"maya.R","clawd":"clawd.R","bit":"bit.R","null":"null.R"}[who]
    body={"maya":"maya.R","clawd":"clawd.B","bit":"bit.B","null":"null.B"}[who]
    arm={"maya":("maya.armL","maya.armR"),"clawd":("clawd.armL","clawd.armR"),"bit":("bit.armL","bit.armR"),"null":("null.armL","null.armR")}[who]
    face={"maya":"maya.eyes","clawd":"clawd.eyes","bit":"bit.eyes","null":"null.eyes"}[who]
    g=f"seg(t,{a},{a+.25})*(1-seg(t,{b-.25},{b}))"
    if act=="turn": w(f"    {obj}.rotation_euler.z+=math.radians({v})*{g}")
    elif act=="jump": w(f"    {body}.location.z+=abs(math.sin(seg(t,{a},{b})*math.pi*{ev.get('n',2)}))*{v*.1}")
    elif act=="armsup": w(f"    {arm[0]}.rotation_euler.x+=-2.6*{g}; {arm[1]}.rotation_euler.x+=-2.6*{g}")
    elif act=="shake": w(f"    {obj}.location.x+=math.sin(t*60)*.006*{g}")
    elif act=="lean": w(f"    {body}.rotation_euler.x+={v}*{g}")
    elif act=="wide": w(f"    {face}.scale.z=1.5 if {a}<=t<{b} else {face}.scale.z")
    elif act=="move": w(f"    {obj}.location.x+={v}*ease(seg(t,{a},{a+.8}))*(1-ease(seg(t,{b-.8},{b})))")
    elif act=="shrink": w(f"    {obj}.scale=(1-{v}*seg(t,{a},{b}),)*3")
    elif act=="fall": w(f"    {obj}.rotation_euler.x+=-1.4*seg(t,{a},{a+.5})*{v}; {obj}.location.z-=.0*seg(t,{a},{b})")
# infection: eyes + body flicker between orange and red/black
for a,b in C.get("infect",[]):
    w(f"    inf=(seg(t,{a},{a+.3})*(1-seg(t,{b-.3},{b})))*(1 if int(t*10)%3 else .3)")
    w("    rEyes.hide_render=(inf<.5); clawd.eyes.hide_render=(inf>=.5)")
    w("    cc=[ORA[i]*(1-inf)+(.9,.02,.02)[i]*inf for i in range(3)]; CMAT.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*cc,1)")
if C.get("infect"):
    pass
for a,b in C.get("blackout_clawd",[]):
    w(f"    bk=seg(t,{a},{a+.8}); cc=[ORA[i]*(1-bk)+(.01,.01,.01)[i]*bk for i in range(3)]; CMAT.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*cc,1)")
for a,b,f0,f1 in C.get("clawd_black",[]):
    w(f"    if {a}<=t<{b}:\n        bk={f0}+({f1}-{f0})*seg(t,{a},{b}); cc=[ORA[i]*(1-bk)+(.01,.01,.01)[i]*bk for i in range(3)]; CMAT.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*cc,1)")
for a,b in C.get("alpha_gold",[]):
    w(f"    ag=seg(t,{a},{a+1.5}); bpy.data.materials['alpham'].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.5+.45*ag,.02+.6*ag,.02+.05*ag,1)")
for a,b in C.get("purple_null",[]):
    w(f"    pu=seg(t,{a},{a+1.2}); NM=bpy.data.materials['nullm'].node_tree.nodes['Principled BSDF'].inputs['Base Color']; NM.default_value=(.015+.5*pu,.012+.1*pu,.015+.8*pu,1); REDE.node_tree.nodes['Principled BSDF'].inputs['Emission Color'].default_value=(1-.5*pu,.03+.1*pu,.03+.9*pu,1)")
if C.get("confetti"):
    t0=C["confetti"]
    w(f"    for o,v0,rt in CONF:\n        tt=max(0,t-{t0}); o.hide_render=t<{t0}; o.location=Vector((.55,.6,.5))+Vector((v0.x*tt*.9,v0.y*tt*.4,v0.z*tt*.6-1.6*tt*tt)); o.rotation_euler=rt*tt")
if C.get("door"):
    a=C["door"]
    w(f"    DRH.rotation_euler.z=-1.5*eo(seg(t,{a},{a+.5})); DL.data.energy={900*C.get('door_gain',1)}*seg(t,{a},{a+.5}); DLM.node_tree.nodes['Principled BSDF'].inputs['Emission Strength'].default_value={40*C.get('door_gain',1)}*seg(t,{a},{a+.5})")
w("render_loop(animate)")
open(f"d{D}.py","w").write("\n".join(out)+"\n")
open(f"run{D}.py","w").write(open("lib.py").read()+"\n"+open(f"d{D}.py").read())
print("scene ok",D)
