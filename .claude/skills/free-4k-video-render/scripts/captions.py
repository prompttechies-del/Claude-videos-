"""Bold Reel captions (ASS) timed across each narration line.
Usage: python captions.py <lines.json> <out.ass> [y=1440]
lines.json: [{"start": 0.4, "dur": 2.4, "text": "It's midnight.", "hl": {"MIDNIGHT": "Y"}}]  (Y = yellow, B = blue)
Coordinates are for 1080x1920; libass scales them to any output size (4K included)."""
import sys, json
L = json.load(open(sys.argv[1])); y = int(sys.argv[3]) if len(sys.argv) > 3 else 1440
col = {"Y": "&H0000D4FF&", "B": "&H00FF8A2F&"}
ts = lambda x: f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"
ev = []
for l in L:
    chunks, cur = [], []
    for w in l["text"].split():
        cur.append(w)
        if len(cur) == 3 or w[-1] in ".,?!": chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    tot = sum(len(" ".join(c)) + 2 for c in chunks); t = l["start"]
    for c in chunks:
        dd = l["dur"] * (len(" ".join(c)) + 2) / tot; parts = []
        for w in c:
            W = w.upper().strip(".,?!"); disp = w.upper().rstrip(",")
            parts.append("{\\c" + col[l["hl"][W]] + "}" + disp + "{\\c&H00FFFFFF&}" if W in l.get("hl", {}) else disp)
        ev.append(f"Dialogue: 0,{ts(t)},{ts(t + dd)},Cap,,0,0,0,,{{\\pos(540,{y})\\fscx78\\fscy78\\t(0,90,\\fscx104\\fscy104)\\t(90,160,\\fscx100\\fscy100)}}" + " ".join(parts)); t += dd
open(sys.argv[2], "w").write("""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Big Shoulders,138,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,1,0,0,0,100,100,1,0,1,7,4,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(ev) + "\n")
print(len(ev), "captions ->", sys.argv[2])
