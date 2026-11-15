# usage: python3 voice.py DAY   (reads v<DAY>/spec.json: {"lines":[[who,text,(pause_before)]], "tail":2.5})
import sys, json, subprocess, numpy as np, soundfile as sf, os
from kokoro_onnx import Kokoro
D=sys.argv[1]; V=f"v{D}"; sp=json.load(open(f"{V}/spec.json"))
k=Kokoro("../d2v/kokoro-v1.0.onnx","../d2v/voices-v1.0.bin")
VO={"maya":("bf_emma",1.0,"en-gb",None),"clawd":("af_heart",1.02,"en-us",None),"bit":("am_puck",1.08,"en-us","asetrate=24000*1.32,aresample=24000,"),
    "null":("am_michael",.82,"en-us","asetrate=24000*0.82,aresample=24000,"),"vance":("bm_george",.98,"en-gb",None),"clone":("af_heart",1.02,"en-us",None),"creator":("bm_lewis",.95,"en-gb",None),"chorus":("af_nicole",.9,"en-us","asetrate=24000*0.78,aresample=24000,")}
FX="highpass=f=75,lowpass=f=13000,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=3,alimiter=limit=0.9"
t=float(sp.get("first",.3)); out=[]; sr=44100
for i,L in enumerate(sp["lines"]):
    who,text=L[0],L[1]; pause=L[2] if len(L)>2 else .35
    v,spd,lang,pre=VO[who]; a,r=k.create(text,voice=v,speed=spd,lang=lang); sf.write(f"{V}/raw{i}.wav",a,r)
    fx=(pre or "")+FX+(",aecho=0.8:0.7:60|120:0.4|0.3,vibrato=f=7:d=0.3" if who in ("null","chorus") else "")+(",volume=0.8,highpass=f=200" if (len(L)>3 and L[3]=="whisper") else "")
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{V}/raw{i}.wav","-af",fx,"-ar","44100","-ac","1",f"{V}/l{i}.wav"],check=True)
    d=sf.info(f"{V}/l{i}.wav").duration
    if i: t+=pause
    out.append({"who":who,"text":text,"start":round(t,2),"dur":round(d,2)}); t+=d
T=round(t+sp.get("hold",1.2)+sp.get("tail",2.5),2); T3=round(t+sp.get("hold",1.2),2)
mix=np.zeros(int(T*sr)); FPS=24; env={}
for i,l in enumerate(out):
    a,_=sf.read(f"{V}/l{i}.wav"); j=int(l["start"]*sr); mix[j:j+len(a)]+=a[:len(mix)-j]
    e=env.setdefault(l["who"],[0.0]*int(T*FPS))
    for f in range(int(len(a)/sr*FPS)):
        s=a[int(f/FPS*sr):int((f+1)/FPS*sr)]; e[int(l["start"]*FPS)+f]=float(np.sqrt((s**2).mean()))
for w in env: m=max(env[w]) or 1; env[w]=[round(x/m*1.6,3) for x in env[w]]
sf.write(f"{V}/voice_mix.wav",mix,sr)
json.dump({"lines":out,"T":T,"T3":T3,"start":[l["start"] for l in out],"env":env},open(f"{V}/timing.json","w"))
for l in out: print(l["start"],round(l["start"]+l["dur"],2),l["who"],l["text"])
print("T3",T3,"T",T)
