#!/usr/bin/env bash
# Check every tool the Reel pipeline needs before a long render, so it does not fail halfway. Prints OK/MISSING per item.
R=$(git rev-parse --show-toplevel 2>/dev/null || pwd); bad=0
chk(){ if eval "$2" >/dev/null 2>&1; then echo "OK       $1"; else echo "MISSING  $1  -> $3"; bad=1; fi; }
chk "blender"            "blender --version"                      "bash .claude/skills/blender-reel-3d/scripts/setup.sh"
chk "libEGL (headless)"  "ldconfig -p | grep -q libEGL.so.1"      "apt-get install -y libegl1"
chk "ffmpeg"             "ffmpeg -version"                        "apt-get install -y ffmpeg"
chk "chromium"           "ls /opt/pw-browsers/chromium-*/chrome-linux/chrome" "preinstalled in the cloud container"
chk "playwright-core"    "test -d $HOME/.cache/free-4k/node_modules/playwright-core" "see free-4k-video-render SKILL.md setup"
chk "kokoro voice"       "python3 -c 'import kokoro_onnx'"        "pip install kokoro-onnx"
chk "numpy + PIL"        "python3 -c 'import numpy, PIL'"         "pip install numpy pillow"
chk "brand logos"        "test -f $R/assets/brand-logos/index.json" "assets/brand-logos (Simple Icons)"
chk "disk space > 5 GB"  "test \$(df --output=avail -k . | tail -1) -gt 5000000" "delete old frame folders"
exit $bad
