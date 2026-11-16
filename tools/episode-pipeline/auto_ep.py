# usage: python3 auto_ep.py ID   (reads v<ID>/day.json; builds voices, screens, ep.json, cards.json, overlay, scene, sfx)
import sys, json, subprocess, os
sys.path.insert(0,"."); from scrimg import *; from vcall import call
ID=sys.argv[1]; V=f"v{ID}"; os.makedirs(V,exist_ok=True)
J=json.load(open(f"{V}/day.json"))
json.dump({"lines":J["lines"],"hold":J.get("hold",2.4),"tail":2.6,"first":J.get("first",.3)},open(f"{V}/spec.json","w"))
if not os.path.exists(f"{V}/timing.json") or J.get("revoice"):
    subprocess.run(["python3","voice.py",ID],check=True,stdout=subprocess.DEVNULL)
tm=json.load(open(f"{V}/timing.json")); L=tm["lines"]; T3=tm["T3"]
def ls(i): return L[min(i,len(L)-1)]["start"]
def le(i): i=min(i,len(L)-1); return L[i]["start"]+L[i]["dur"]
# ---- screens ----
imgs={}; scr=[]; call_prefix=None
for n,s in enumerate(J.get("screens",[])):
    k=s["kind"]; pre=f"sc{n}"; at=ls(s["at"]); to=le(s.get("to",s["at"]))
    if k=="typed":
        rows=[(t,tuple(int(c[i:i+2],16) for i in (1,3,5)),MO(38),74) for t,c in s["rows"]]
        typed(f"{V}/{pre}",s["title"],rows); imgs[pre]=[pre,25]; scr.append({"t":round(at,2),"img":pre,"seq":[round(at+.3,2),round(to-.4,2)]})
    elif k=="big":
        red=s.get("red",False); im=Image.new("RGB",(1024,600),(20,2,4) if red else (14,18,30)); d=ImageDraw.Draw(im); d.rectangle((0,0,1024,62),fill=(60,10,14) if red else (24,32,56)); d.text((512,10),s["title"],font=BS(40),fill=(230,235,255),anchor="ma")
        c=tuple(int(s["col"][i:i+2],16) for i in (1,3,5)); y=130
        for line in s["text"].split("|"): d.text((512,y),line,font=BS(s.get("size",110)),fill=c,anchor="ma"); y+=s.get("size",110)*1.1
        ImageOps.flip(im).save(f"{V}/{pre}_00.png"); imgs[pre]=[pre,1]; scr.append({"t":round(at,2),"img":pre,"idx":0})
    elif k=="list":
        im=Image.new("RGB",(1024,600),(14,18,30)); d=ImageDraw.Draw(im); d.rectangle((0,0,1024,62),fill=(24,32,56)); d.text((512,10),s["title"],font=BS(40),fill=(230,235,255),anchor="ma")
        for i,(t,c) in enumerate(s["items"]): d.text((50,95+i*70),t,font=MO(34),fill=tuple(int(c[j:j+2],16) for j in (1,3,5)))
        ImageOps.flip(im).save(f"{V}/{pre}_00.png"); imgs[pre]=[pre,1]; scr.append({"t":round(at,2),"img":pre,"idx":0})
    elif k=="cols":
        im=Image.new("RGB",(1024,600),(14,18,30)); d=ImageDraw.Draw(im); d.rectangle((0,0,1024,62),fill=(24,32,56)); d.text((512,10),s["title"],font=BS(40),fill=(230,235,255),anchor="ma")
        for x0,(ttl,items,c) in ((30,s["left"]),(534,s["right"])):
            cc=tuple(int(c[j:j+2],16) for j in (1,3,5)); d.rounded_rectangle((x0,90,x0+460,520),16,fill=(26,32,50),outline=cc,width=4); d.text((x0+230,110),ttl,font=BS(60),fill=cc,anchor="ma")
            for i,t in enumerate(items): d.text((x0+24,220+i*70),"• "+t,font=MO(26),fill=(225,230,240))
        ImageOps.flip(im).save(f"{V}/{pre}_00.png"); imgs[pre]=[pre,1]; scr.append({"t":round(at,2),"img":pre,"idx":0})
    elif k=="call":   # video call with Vance; mouth sync from the vance voice
        for m in range(3): call(f"{V}/{pre}_{m:02d}.png",m)
        call(f"{V}/{pre}_03.png",state="null"); call(f"{V}/{pre}_04.png",state="dropped"); imgs[pre]=[pre,5]
        scr.append({"t":round(at,2),"img":pre,"mouth":"vance"} if not s.get("state") else {"t":round(at,2),"img":pre,"idx":{"null":3,"dropped":4}[s["state"]]})
# ---- shots ----
shots=[]; sh=J["shots"]
for i,x in enumerate(sh):
    a=0 if i==0 else ls(x["at"]); b=(ls(sh[i+1]["at"]) if i+1<len(sh) else 99); shots.append([round(a,2),round(b,2),x["pre"]])
# ---- cards ----
cards=[]; labn=0
for x in J.get("cards",[]):
    a=ls(x["at"])+x.get("off",.2); b=le(x.get("to",x["at"]))+x.get("hold",.3)
    c={"k":x["k"],"txt":x.get("txt",""),"t":[round(a,2),round(min(b,T3),2)]}
    for key in ("col","size","y","shake","rot","items"): 
        if key in x: c[key]=x[key]
    if x["k"]=="lab": c["x"]=x.get("x",90+(labn%3)*160); c["y"]=x.get("y",300+labn*130); labn+=1
    if x["k"]=="lab" and "col" not in c: c["col"]="#FFC233"
    cards.append(c)
cj={"cards":cards,"end1":J["end"][0],"end2":J["end"][1]}
json.dump(cj,open(f"{V}/cards.json","w"))
# ---- ep ----
ep={"cast":J["cast"],"images":imgs,"screens":scr,"shots":shots,"pad":J.get("pad",[196,247,294])}
def win(lst,fn):
    return [[round(ls(w["at"]),2),round(le(w.get("to",w["at"]))+.2,2)]+fn(w) for w in lst]
if J.get("alert"): ep["alert"]=win(J["alert"],lambda w:[w.get("l",.4)])
if J.get("infect"): ep["infect"]=win(J["infect"],lambda w:[])
if J.get("dark"): ep["dark"]=win(J["dark"],lambda w:[])
if J.get("purple"): ep["purple_null"]=[[0,40]]
if J.get("alpha_gold"): ep["alpha_gold"]=[[round(ls(J["alpha_gold"]),2),99]]
if J.get("clawd_black"): ep["clawd_black"]=[[round(ls(w["at"]),2),round(le(w.get("to",w["at"])),2),w["from"],w["to_"]] for w in J["clawd_black"]]
for key in ("confetti","door"):
    if key in J: ep[key]=round(ls(J[key]),2) if isinstance(J[key],int) else J[key]
if "door_gain" in J: ep["door_gain"]=J["door_gain"]
if J.get("null_in_clawd"): ep["null_in_clawd"]=True
ev=[]
for e in J.get("events",[]):
    ev.append({"t":[round(ls(e["at"])+e.get("off",0),2),round(le(e.get("to",e["at"])),2)],"who":e["who"],"act":e["act"],**({"v":e["v"]} if "v" in e else {}),**({"n":e["n"]} if "n" in e else {})})
ep["events"]=ev
json.dump(ep,open(f"{V}/ep.json","w"))
for step in (["gen_overlay.py"],["gen_scene.py"],["gen_sfx.py"]): subprocess.run(["python3",step[0],ID],check=True,stdout=subprocess.DEVNULL)
print("built",ID,"T3",T3)
