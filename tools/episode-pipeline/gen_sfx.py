# usage: python3 gen_sfx.py DAY  (auto sound design from cards.json + ep.json)
import sys,json; sys.path.insert(0,".")
from sfxlib import *
D=sys.argv[1]; tm=json.load(open(f"v{D}/timing.json")); cards=json.load(open(f"v{D}/cards.json"))["cards"]; C=json.load(open(f"v{D}/ep.json"))
T,T3=tm["T"],tm["T3"]; m=Mix(T); m.add(0,pad(T3-1,tuple(C.get("pad",(196,247,294)))),.1)
for x in cards:
    a=x["t"][0]; k=x["k"]
    if k in("s",): m.add(a-.05,whoosh(.3),.3)
    elif k=="b": m.add(a,hit(70,.35),.55 if x.get("col","")!="#FF3B3B" else .8); m.add(a-.08,whoosh(.25),.35)
    elif k in("m","lab","logos"): m.add(a-.05,whoosh(.25),.3); m.add(a+.1,thud(.2),.5); m.add(a+.12,pop(800+(int(a*10)%5)*120,.08),.4)
    elif k=="card": m.add(a,pop(900,.1),.4)
for s in C.get("screens",[]):
    if "seq" in s:
        a,b=s["seq"]; m.add(a,typing(max(.5,b-a),12),.3)
for a,b,l in C.get("alert",[]):
    m.add(a,glitch(.3),.5); m.add(a,drone(min(b-a,6),44),.5)
for a,b in C.get("infect",[]):
    m.add(a,glitch(.5),.6); m.add(a,drone(min(b-a,5),40),.5)
    for i in range(int((b-a)/.5)): m.add(a+i*.5,glitch(.06),.35)
for a,b in C.get("dark",[]): m.add(a,hit(40,.9),1.0); m.add(a,whoosh(.6),.4)
if C.get("confetti"): 
    t0=C["confetti"]; m.add(t0,hit(70,.4),.7)
    for i in range(30): m.add(t0+.05+i*.04,pop(1200+i*30,.05),.3)
if C.get("door"): a=C["door"]; m.add(a-.1,hit(40,.9),1.0); m.add(a,whoosh(.8),.6)
endcard(m,T3); m.save(f"v{D}/sfx.wav"); print("sfx ok")
