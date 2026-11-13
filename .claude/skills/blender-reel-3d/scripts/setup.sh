#!/usr/bin/env bash
# Install Blender and the libraries it needs to render without a screen (Ubuntu/Debian, run as root).
set -e
command -v blender >/dev/null || { apt-get update -qq; DEBIAN_FRONTEND=noninteractive apt-get install -y -qq blender; }
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq libegl1 libgl1 libgles2 >/dev/null
blender --version | head -1
