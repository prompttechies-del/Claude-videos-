#!/usr/bin/env bash
# render4k.sh: one command from a source (Remotion project, HTML file, frames folder or video) to a finished file.
#   render4k.sh --src <path> [--orientation 16x9|9x16|1x1] [--fps 30] [--quality draft|standard|master]
#               [--gpu auto|nvidia|amd|intel|apple|none] [--duration SEC] [--comp ID] [--audio FILE]
#               [--captions FILE.srt|.ass] [--out FILE] [--force]
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=""; ORI=16x9; FPS=30; QUALITY=standard; GPU=auto; DUR=""; COMP=""; OUT=""; AUDIO=""; CAPS=""; FORCE=0
usage(){ sed -n '2,5p' "$0" | sed 's/^# \{0,1\}//'; }
while [ $# -gt 0 ]; do case "$1" in
  --src) SRC=$2; shift 2;; --orientation) ORI=$2; shift 2;; --fps) FPS=$2; shift 2;; --quality) QUALITY=$2; shift 2;;
  --gpu) GPU=$2; shift 2;; --duration) DUR=$2; shift 2;; --comp) COMP=$2; shift 2;; --audio) AUDIO=$2; shift 2;;
  --captions) CAPS=$2; shift 2;; --out) OUT=$2; shift 2;; --force) FORCE=1; shift;; -h|--help) usage; exit 0;;
  *) echo "unknown flag: $1" >&2; usage; exit 2;; esac; done
[ -n "$SRC" ] && [ -e "$SRC" ] || { echo "❌ --src is required and must exist" >&2; exit 2; }
case "$QUALITY" in draft) L=1920; S=1080; CRF=26; PRESET=ultrafast;; standard) L=3840; S=2160; CRF=18; PRESET=veryfast;;
  master) L=3840; S=2160; CRF=14; PRESET=slow;; *) echo "❌ --quality must be draft|standard|master" >&2; exit 2;; esac
case "$ORI" in 16x9) W=$L; H=$S;; 9x16) W=$S; H=$L;; 1x1) W=$S; H=$S;; *) echo "❌ --orientation must be 16x9|9x16|1x1" >&2; exit 2;; esac

# ---- source type
if [ -d "$SRC" ] && [ -f "$SRC/package.json" ] && grep -q '"remotion"' "$SRC/package.json"; then TYPE=remotion
elif [ -f "$SRC" ] && [[ "$SRC" =~ \.[hH][tT][mM][lL]?$ ]]; then TYPE=html
elif [ -d "$SRC" ] && ls "$SRC" | grep -qiE '\.(png|jpe?g)$'; then TYPE=frames
elif [ -f "$SRC" ] && ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 "$SRC" >/dev/null 2>&1; then TYPE=video
else echo "❌ could not tell what $SRC is (Remotion project, .html, frames folder or video)" >&2; exit 2; fi

# ---- output path and render cache (hash of source state + flags)
BASE=$(basename "${SRC%/}"); BASE=${BASE%.*}
[ -n "$OUT" ] || OUT="out/${BASE}-${ORI}-${QUALITY}.mp4"
mkdir -p "$(dirname "$OUT")" out/.render-cache
if [ -d "$SRC" ]; then STATE=$(cd "$SRC" && find . -type f -not -path './node_modules/*' -not -path './out/*' -not -path './.git/*' -printf '%P %s %T@\n' | sort); else STATE=$(stat -c '%s %Y' "$SRC"); fi
EXTRA_STATE=""; for f in "$AUDIO" "$CAPS"; do [ -n "$f" ] && EXTRA_STATE+=$(stat -c '%n %s %Y' "$f"); done
KEY=$(printf '%s|%s|%s|%s|%s|%s|%s|%s|%s' "$STATE" "$ORI" "$FPS" "$QUALITY" "$DUR" "$COMP" "$EXTRA_STATE" "$SRC" "$OUT" | sha1sum | cut -c1-16)
if [ $FORCE = 0 ] && [ -f "out/.render-cache/$KEY" ] && [ -s "$OUT" ]; then echo "⏩ unchanged since last render (cache $KEY): $OUT   (--force to re-render)"; exec python3 "$HERE/verify.py" "$OUT" --w $W --h $H --fps "$FPS"; fi
WORK="out/.work/$KEY"; mkdir -p "$WORK"; T0=$(date +%s)

# ---- encoder: try hardware in order, fall back to libx264. master stays in software for 10-bit H.264.
works(){ ffmpeg -v error -f lavfi -i color=s=256x256:d=0.2 -c:v "$1" -f null - >/dev/null 2>&1; }
ENC=libx264
if [ "$QUALITY" != master ]; then case "$GPU" in
  auto) if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1 && works h264_nvenc; then ENC=h264_nvenc
        elif [ "$(uname)" = Darwin ] && works h264_videotoolbox; then ENC=h264_videotoolbox
        elif works h264_qsv; then ENC=h264_qsv; elif works h264_amf; then ENC=h264_amf; fi;;
  nvidia) works h264_nvenc && ENC=h264_nvenc;; apple) works h264_videotoolbox && ENC=h264_videotoolbox;;
  intel) works h264_qsv && ENC=h264_qsv;; amd) works h264_amf && ENC=h264_amf;; none) ;;
  *) echo "❌ --gpu must be auto|nvidia|amd|intel|apple|none" >&2; exit 2;; esac
  [ "$GPU" != auto ] && [ "$GPU" != none ] && [ "$ENC" = libx264 ] && echo "⚠️  $GPU encoder not usable here; using libx264"; fi
case "$ENC" in
  libx264) VENC=(-c:v libx264 -crf $CRF -preset $PRESET); [ "$QUALITY" = master ] && VENC+=(-pix_fmt yuv420p10le -profile:v high10) || VENC+=(-pix_fmt yuv420p);;
  h264_nvenc) VENC=(-c:v h264_nvenc -rc vbr -cq $CRF -b:v 0 -preset p5 -pix_fmt yuv420p);;
  h264_videotoolbox) VENC=(-c:v h264_videotoolbox -q:v $((100 - CRF * 2)) -pix_fmt yuv420p);;
  h264_qsv) VENC=(-c:v h264_qsv -global_quality $CRF -pix_fmt nv12);;
  h264_amf) VENC=(-c:v h264_amf -rc cqp -qp_i $CRF -qp_p $CRF -pix_fmt yuv420p);; esac
echo "▶ $TYPE → ${W}x${H} @ ${FPS} fps, $QUALITY, encoder $ENC${DUR:+, first ${DUR}s}"

# ---- stage 1: get pixels
case "$TYPE" in
  frames) FIRST=$(ls "$SRC" | grep -iE '\.(png|jpe?g)$' | sort | head -1); EXT=${FIRST##*.}; PROBE="$SRC/$FIRST"
          INARGS=(-framerate "$FPS" -pattern_type glob -i "$SRC/*.$EXT");;
  video)  PROBE="$SRC"; INARGS=(-i "$SRC");;
  html)   NODE_DIR="${FREE4K_NODE:-$HOME/.cache/free-4k/node_modules}"
          [ -d "$NODE_DIR/playwright-core" ] || { echo "  installing playwright-core (once)…"; npm install --silent --no-audit --no-fund --prefix "$(dirname "$NODE_DIR")" playwright-core@${PLAYWRIGHT_VERSION:-1.56.0} >/dev/null; }
          # logical page is 1080p-sized; 4K comes from device scale 2, so layouts in px stay the same at every quality
          case "$ORI" in 16x9) PW=1920; PH=1080;; 9x16) PW=1080; PH=1920;; 1x1) PW=1080; PH=1080;; esac
          rm -rf "$WORK/frames"; node "$HERE/html2frames.mjs" --src "$SRC" --out "$WORK/frames" --w $PW --h $PH --scale $((W / PW)) --fps "$FPS" ${DUR:+--duration "$DUR"} $([ "$QUALITY" = master ] && echo --png)
          EXT=$([ "$QUALITY" = master ] && echo png || echo jpg); PROBE="$WORK/frames/f000000.$EXT"; INARGS=(-framerate "$FPS" -i "$WORK/frames/f%06d.$EXT"); DUR="";;
  remotion) ENTRY=""; for e in src/index.ts src/index.tsx src/index.js src/index.jsx remotion/index.ts; do [ -f "$SRC/$e" ] && { ENTRY=$e; break; }; done
          [ -n "$ENTRY" ] || { echo "❌ no Remotion entry (src/index.ts) in $SRC" >&2; exit 2; }
          [ -d "$SRC/node_modules" ] || (cd "$SRC" && npm install --no-audit --no-fund >/dev/null)
          [ -n "$COMP" ] || COMP=$(cd "$SRC" && npx remotion compositions "$ENTRY" --quiet 2>/dev/null | tr ' ' '\n' | grep -v '^$' | head -1)
          [ -n "$COMP" ] || { echo "❌ pass --comp <composition id>" >&2; exit 2; }
          RS=${REMOTION_SCALE:-$([ "$QUALITY" = draft ] && echo 1 || echo 2)}; ABS="$(pwd)/$WORK/remotion.mp4"
          (cd "$SRC" && npx remotion render "$ENTRY" "$COMP" "$ABS" --scale="$RS" --concurrency="$(nproc)" --crf=12 ${DUR:+--frames=0-$(( ${DUR%.*} * FPS - 1 ))} --log=error)
          PROBE="$WORK/remotion.mp4"; INARGS=(-i "$WORK/remotion.mp4"); DUR="";;
esac

# ---- stage 2: conform to the target frame, finish, encode
SW=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$PROBE"); SH=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$PROBE")
SAME=$(awk -v a=$SW -v b=$SH -v c=$W -v d=$H 'BEGIN{r=(a/b)/(c/d); print (r>0.99 && r<1.01) ? 1 : 0}')
UP=$(awk -v a=$SW -v c=$W 'BEGIN{print (c > a*1.2) ? 1 : 0}')
if [ "$SAME" = 1 ]; then VF="[0:v]scale=$W:$H:flags=lanczos"
else VF="[0:v]split[a][b];[a]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,boxblur=40[bg];[b]scale=$W:$H:force_original_aspect_ratio=decrease:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2"; fi
[ "$UP" = 1 ] && VF+=",unsharp=5:5:0.6"
VF+=",fps=$FPS,setsar=1"
if [ -n "$CAPS" ]; then ESC=$(printf '%s' "$CAPS" | sed "s/[\\\\:',]/\\\\&/g")
  if [[ "$CAPS" =~ \.ass$ ]]; then VF+=",ass=$ESC"; else VF+=",subtitles=$ESC:force_style='FontName=Inter,FontSize=18,Bold=1,Outline=2,Alignment=2,MarginV=120'"; fi; fi
VF+="[v]"
AARGS=(-an); WANT_AUDIO=no
LOUD="loudnorm=I=-14:TP=-1.5:LRA=11"
if [ -n "$AUDIO" ]; then INARGS+=(-i "$AUDIO"); AARGS=(-map 1:a:0 -af "$LOUD" -ar 48000 -c:a aac -b:a 192k -shortest); WANT_AUDIO=yes
elif [ "$TYPE" = video ] || [ "$TYPE" = remotion ]; then
  if ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 "$PROBE" | grep -q .; then AARGS=(-map 0:a:0 -af "$LOUD" -ar 48000 -c:a aac -b:a 192k); WANT_AUDIO=yes; fi; fi
ffmpeg -v error -stats -y "${INARGS[@]}" -filter_complex "$VF" -map "[v]" "${AARGS[@]}" ${DUR:+-t "$DUR"} "${VENC[@]}" -movflags +faststart "$OUT"

if [ "$QUALITY" = master ]; then   # archive copy: HEVC 10-bit by default, ProRes 422 HQ with MASTER_COPY=prores (very large)
  if [ "${MASTER_COPY:-hevc}" = prores ]; then ffmpeg -v error -y -i "$OUT" -c:v prores_ks -profile:v 3 -pix_fmt yuv422p10le -c:a pcm_s16le "${OUT%.mp4}-prores.mov"; echo "  + ${OUT%.mp4}-prores.mov"
  else ffmpeg -v error -y -i "$OUT" -c:v libx265 -crf 16 -preset medium -pix_fmt yuv420p10le -tag:v hvc1 -c:a copy "${OUT%.mp4}-hevc.mp4"; echo "  + ${OUT%.mp4}-hevc.mp4"; fi; fi
echo "$OUT" > "out/.render-cache/$KEY"; rm -rf "$WORK"
echo "⏱  $(( $(date +%s) - T0 )) s"
python3 "$HERE/verify.py" "$OUT" --w $W --h $H --fps "$FPS" --audio $WANT_AUDIO
