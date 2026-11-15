import sys; sys.path.insert(0,"."); from scrimg import *
def call(path,mouth=0,state="ok",title="VIDEO CALL · Mr. Vance"):
    bg=(10,12,20) if state!="null" else (20,0,4)
    im=Image.new("RGB",(1024,600),bg); d=ImageDraw.Draw(im); d.rectangle((0,0,1024,62),fill=(24,32,56) if state!="null" else (60,10,14)); d.text((30,12),title,font=BS(40),fill=(230,235,255)); d.ellipse((960,20,984,44),fill=(255,50,50))
    if state=="dropped": d.text((512,260),"CALL ENDED",font=BS(110),fill=(255,60,60),anchor="mm"); ImageOps.flip(im).save(path); return
    if state=="slides": d.text((512,300),"SLIDE 3 · FROZEN ❄",font=BS(90),fill=(120,170,255),anchor="mm"); d.text((512,420),"not responding...",font=MO(32),fill=(170,180,210),anchor="mm"); ImageOps.flip(im).save(path); return
    d.rectangle((60,80,964,540),fill=(60,70,90) if state!="null" else (25,0,4)); V=22; x0=512-7*V; y0=110
    skin=(214,170,135) if state!="null" else (16,10,12)
    for i in range(14):
        for j in range(14): d.rectangle((x0+i*V,y0+j*V,x0+i*V+V-2,y0+j*V+V-2),fill=skin)
    if state!="null":
        for i in range(14):
            for j in range(3): d.rectangle((x0+i*V,y0+j*V,x0+i*V+V-2,y0+j*V+V-2),fill=(150,150,155))
        for x in (x0+3*V,x0+9*V): d.rectangle((x,y0+5*V,x+2*V-2,y0+7*V-2),fill=(250,250,250)); d.rectangle((x+V//2,y0+5*V+4,x+V+6,y0+7*V-6),fill=(30,30,40))
        mh=[6,18,34][mouth]; d.rectangle((x0+5*V,y0+10*V,x0+9*V,y0+10*V+mh),fill=(110,40,40)); d.rectangle((x0,y0+14*V,x0+14*V,540),fill=(40,45,60))
    else:
        for x in (x0+3*V,x0+9*V): d.rectangle((x,y0+5*V,x+2*V-2,y0+7*V),fill=(255,30,30))
        d.arc((x0+4*V,y0+7*V,x0+10*V,y0+11*V),20,160,fill=(255,30,30),width=10)
    ImageOps.flip(im).save(path)
