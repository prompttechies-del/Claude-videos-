"""Build the Prompt Techies Reel overlays at a given scale (1 = 1080x1920, 2 = 4K 2160x3840).
Usage: python brand.py <outdir> <scale> "<TITLE>" "<TAG>" """
import sys, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out, s, TITLE, TAG = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, "..", "assets")
FD = "/mnt/skills/examples/canvas-design/canvas-fonts/"
BIG = FD + "BigShoulders-Bold.ttf" if os.path.exists(FD + "BigShoulders-Bold.ttf") else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = FD + "BricolageGrotesque-Bold.ttf" if os.path.exists(FD + "BricolageGrotesque-Bold.ttf") else BIG
os.makedirs(out, exist_ok=True)
logo = Image.open(os.path.join(A, "prompt-techies-logo.png")).convert("RGBA"); W, H = logo.size
icon = logo.crop((0, 0, W, int(H * 0.80))); icon = icon.crop(icon.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
sc = lambda im, h: im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

def glowed(im, r, col, alpha):
    pad = r * 3; o = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    g = Image.new("RGBA", o.size, (0, 0, 0, 0)); g.paste(col + (alpha,), (pad, pad), im.getchannel("A")); g = g.filter(ImageFilter.GaussianBlur(r))
    o.alpha_composite(g); o.alpha_composite(im, (pad, pad)); return o

# top-right logo icon
glowed(sc(icon, 108 * s), 6 * s, (255, 255, 255), 130).save(f"{out}/icon.png")
# bottom wordmark: icon + "Prompt Techies" in brush script, cyan-to-blue gradient, thin white edge, blue glow
f = ImageFont.truetype(os.path.join(A, "KaushanScript-Regular.ttf"), 48 * s); ic = sc(icon, 48 * s); t = "Prompt Techies"; tw = int(f.getlength(t)); th = 64 * s
m = Image.new("L", (tw + 8 * s, th), 0); ImageDraw.Draw(m).text((2 * s, th // 2), t, font=f, fill=255, anchor="lm")
edge = Image.new("L", m.size, 0); ImageDraw.Draw(edge).text((2 * s, th // 2), t, font=f, fill=255, anchor="lm", stroke_width=max(1, int(1.6 * s)))
x = np.linspace(0, 1, m.width)[None, :] * np.ones((th, 1)); c0, c1 = np.array([25, 200, 250]), np.array([25, 110, 255])
grad = (c0 * (1 - x[..., None]) + c1 * x[..., None]).astype(np.uint8)
txt = Image.new("RGBA", m.size, (255, 255, 255, 0)); txt.putalpha(edge); txt.alpha_composite(Image.fromarray(np.dstack([grad, np.asarray(m)]), "RGBA"))
mk = Image.new("RGBA", (ic.width + 10 * s + txt.width, th), (0, 0, 0, 0)); mk.alpha_composite(ic, (0, (th - ic.height) // 2)); mk.alpha_composite(txt, (ic.width + 10 * s, 0))
glowed(mk, 9 * s, (40, 150, 255), 140).save(f"{out}/mark.png")
# title box (white, blue underside) and tag (blue)
f = ImageFont.truetype(BIG, 96 * s); tw = int(f.getlength(TITLE)); w, h = tw + 90 * s, 140 * s
im = Image.new("RGBA", (w + 20 * s, h + 30 * s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.rounded_rectangle((6 * s, 14 * s, w + 6 * s, h + 14 * s), radius=26 * s, fill=(10, 90, 240, 255)); d.rounded_rectangle((0, 0, w, h), radius=26 * s, fill=(255, 255, 255, 255))
d.text((w / 2, h / 2 + 2 * s), TITLE, font=f, fill=(12, 12, 16), anchor="mm"); im.save(f"{out}/title.png")
f2 = ImageFont.truetype(BIG, 66 * s); tw2 = int(f2.getlength(TAG)); tg = Image.new("RGBA", (tw2 + 60 * s, 96 * s), (0, 0, 0, 0)); d = ImageDraw.Draw(tg)
d.rounded_rectangle((0, 0, tw2 + 60 * s - 1, 96 * s - 1), radius=14 * s, fill=(20, 120, 255, 255)); d.text(((tw2 + 60 * s) / 2, 49 * s), TAG, font=f2, fill=(255, 255, 255), anchor="mm"); tg.save(f"{out}/tag.png")
# end card: white, full logo, "Follow for more AI tips"
CW, CH, lh = 1080 * s, 1920 * s, 680 * s; g = np.linspace(0, 1, CH)[:, None] * np.ones((1, CW))
im = Image.fromarray(np.dstack([255 - 10 * g, 255 - 5 * g, np.full((CH, CW), 255.), np.full((CH, CW), 255.)]).astype(np.uint8), "RGBA")
L = sc(logo.crop(logo.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()), lh); im.alpha_composite(L, ((CW - L.width) // 2, int(CH * 0.43 - L.height / 2)))
d = ImageDraw.Draw(im); d.text((CW / 2, int(CH * 0.43 + L.height / 2 + lh * 0.05)), "Follow for more AI tips", font=ImageFont.truetype(SANS, int(lh * 0.085)), fill=(18, 44, 200), anchor="mt")
im.convert("RGB").save(f"{out}/end.png")
# dark navy background with a soft blue glow, rounded video mask and glowing ring for the 16:9 frame
H2 = 1920 * s; W2 = 1080 * s; y = np.linspace(0, 1, H2)[:, None] * np.ones((1, W2)); xx = np.linspace(-1, 1, W2)[None, :] * np.ones((H2, 1))
bg = np.array([8, 12, 34.]) * (1 - y[..., None]) + np.array([14, 22, 58.]) * y[..., None] + np.exp(-((xx / 0.9) ** 2 + ((y - 0.5) / 0.22) ** 2))[..., None] * np.array([5, 20, 55.])
Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB").save(f"{out}/bg.png")
vw, vh, r = 1040 * s, 585 * s, 28 * s; mm = Image.new("L", (vw, vh), 0); ImageDraw.Draw(mm).rounded_rectangle((0, 0, vw - 1, vh - 1), radius=r, fill=255); mm.save(f"{out}/mask.png")
pad = 24 * s; ring = Image.new("RGBA", (vw + 2 * pad, vh + 2 * pad), (0, 0, 0, 0)); gg = Image.new("RGBA", ring.size, (0, 0, 0, 0))
ImageDraw.Draw(gg).rounded_rectangle((pad, pad, pad + vw, pad + vh), radius=r, outline=(60, 150, 255, 200), width=10 * s); ring.alpha_composite(gg.filter(ImageFilter.GaussianBlur(10 * s)))
ImageDraw.Draw(ring).rounded_rectangle((pad - 2 * s, pad - 2 * s, pad + vw + 2 * s, pad + vh + 2 * s), radius=r + 2 * s, outline=(150, 200, 255, 230), width=3 * s); ring.save(f"{out}/ring.png")
print("brand assets ->", out)
