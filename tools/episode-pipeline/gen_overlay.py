# usage: python3 gen_overlay.py DAY  -> ../mg/day<DAY>o.html  (cards in v<DAY>/cards.json)
import sys, json, html
D=sys.argv[1]; c=json.load(open(f"v{D}/cards.json")); tm=json.load(open(f"v{D}/timing.json"))
s=open("../mg/day03o.html").read()
a=s.index(' <div class="w" id="a1"'); b=s.index(' <div id="end">')
body=""; js=""
for i,x in enumerate(c["cards"]):
    k=x["k"]; t0,t1=x["t"]; id_=f"c{i}"; col=x.get("col","#fff")
    if k=="s": body+=f' <div class="w" id="{id_}" style="top:{x.get("y",300)}px;font:{x.get("size",110)}px IS;color:{col}">{x["txt"]}</div>\n'; js+=f'pop($("{id_}"),t,{t0},{t1},{{ry:0,y:-50}});\n'
    elif k=="b": body+=f' <div class="w" id="{id_}" style="top:{x.get("y",430)}px;font:{x.get("size",160)}px EO;color:{col}">{x["txt"]}</div>\n'; js+=f'pop($("{id_}"),t,{t0},{t1},{{from:2.4,ry:0,d:.22,shake:{x.get("shake",26)},rot:{x.get("rot",-2)}}});\n'
    elif k=="m": body+=f' <div class="w" id="{id_}" style="top:{x.get("y",430)}px;font:{x.get("size",120)}px BS;letter-spacing:8px;color:{col}">{x["txt"]}</div>\n'; js+=f'pop($("{id_}"),t,{t0},{t1},{{ry:80,ph:{i}}});\n'
    elif k=="lab": body+=f' <div class="lab" id="{id_}" style="left:{x["x"]}px;top:{x["y"]}px;color:{col}">{x["txt"]}</div>\n'; js+=f'pop($("{id_}"),t,{t0},{t1},{{ry:{80 if i%2 else -80},ph:{i},y:60}});\n'
    elif k=="logos":
        tiles="".join(f'<span style="display:inline-block;width:230px;height:230px;margin:0 14px;border-radius:40px;background:#fff;position:relative"><span style="position:absolute;inset:48px;background:{h};-webkit-mask:url(assets/{f}.svg) center/contain no-repeat;mask:url(assets/{f}.svg) center/contain no-repeat"></span></span>' for f,h in x["items"])
        body+=f' <div class="w" id="{id_}" style="top:{x.get("y",1450)}px;text-shadow:none">{tiles}</div>\n'; js+=f'pop($("{id_}"),t,{t0},{t1},{{ry:0,y:60,from:.6}});\n'
    elif k=="card": body+=f' <div class="w" id="{id_}" style="top:{x.get("y",250)}px"><span style="display:inline-block;font:40px MO;background:#0b0b10;border:4px solid {col};border-radius:18px;padding:20px 30px;line-height:1.35;white-space:normal;width:860px;text-align:left">{x["txt"]}</span></div>\n'; js+=f'pop($("{id_}"),t,{t0},{t1},{{ry:0,y:-40,from:.8}});\n'
s=s[:a]+body+s[b:]
T,T3=tm["T"],tm["T3"]
s=s.replace("who sent it? →",c["end1"]).replace("DAY 4 DROPS TOMORROW",c["end2"]).replace("DAY 03<span",f"DAY {D}<span").replace("const T=24.5",f"const T={T}")
a=s.index('  pop($("a1")'); b=s.index('  const lt=t-22.0')
s=s[:a]+js+s[b:].replace("const lt=t-22.0",f"const lt=t-{T3}")
FIT = r"""
const __M=document.createElement('span'); __M.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;left:-9999px;top:0'; document.body.appendChild(__M);
function fit(){
  document.querySelectorAll('.w').forEach(el=>{ if(el.children.length) return; const cs=getComputedStyle(el); const o=el.dataset.fs?parseFloat(el.dataset.fs):parseFloat(cs.fontSize); el.dataset.fs=o;
    __M.style.font=cs.font.replace(/[\\d.]+px/,o+'px'); __M.style.letterSpacing=cs.letterSpacing; __M.textContent=el.textContent; const w=__M.offsetWidth; if(w>0) el.style.fontSize=Math.min(o,o*940/w)+'px'; });
  document.querySelectorAll('.lab').forEach(el=>{ const l=parseFloat(el.dataset.l||el.style.left); el.dataset.l=l; const w=el.offsetWidth; el.style.left=(w>0?Math.max(30,Math.min(l,1050-w)):l)+'px'; });
}
"""
s=s.replace('window.frame=function(t){ t=cl(t,0,T-.001);', FIT+'window.frame=function(t){ t=cl(t,0,T-.001); fit();')
open(f"../mg/day{D}o.html","w").write(s); print("ok",T3,T)
