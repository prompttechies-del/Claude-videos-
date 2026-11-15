# helpers to draw monitor images (1024x600, flipped vertically for the screen mapping)
from PIL import Image, ImageDraw, ImageFont, ImageOps
A="/tmp/claude-0/-home-user-Claude-videos-/0301aef4-c249-512f-8dcb-48f473421570/scratchpad/mg/assets/"
BS=lambda s: ImageFont.truetype(A+"BigShoulders-Bold.ttf",s); MO=lambda s: ImageFont.truetype(A+"JetBrainsMono-Bold.ttf",s)
def typed(path_prefix, title, lines, n=24, bg=(14,18,30), bar=(24,32,56), tcol=(230,235,255)):
    # lines: [(text, color, font, line_height)] ; types progressively, centered
    full=sum(len(l[0]) for l in lines)
    for s in range(n+1):
        im=Image.new("RGB",(1024,600),bg); d=ImageDraw.Draw(im); d.rectangle((0,0,1024,62),fill=bar); d.text((512,10),title,font=BS(40),fill=tcol,anchor="ma")
        left=int(full*s/n); y=90
        for t,c,f,lh in lines:
            w=d.textlength(t,font=f); d.text((512-w/2,y),t[:max(0,left)],font=f,fill=c); left-=len(t); y+=lh
        ImageOps.flip(im).save(f"{path_prefix}_{s:02d}.png")
