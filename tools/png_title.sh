#!/bin/bash
# Genera un PNG 1920x1080 con titulo + linea ambar + cita (estilo Goods Uncovered)
# uso: tools/png_title.sh salida.png "TITULO" "cita" [bg]   bg=alpha|black
set -e
SER=/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf
OUT="$1"; TITLE="$2"; QUOTE="$3"; BG="${4:-alpha}"
esc(){ printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e "s/'/’/g" -e 's/:/\\:/g' -e 's/%/\\%/g'; }
T=$(esc "$TITLE"); Q=$(esc "$QUOTE")
if [ "$BG" = black ]; then SRC="color=c=black:s=1920x1080"; else SRC="color=c=black@0.0:s=1920x1080,format=rgba"; fi
ffmpeg -loglevel error -y -f lavfi -i "$SRC" -f lavfi -i "color=c=0xE8A33D:s=860x5" -frames:v 1 -filter_complex "\
[0][1]overlay=x=(W-860)/2:y=575:format=auto,\
drawtext=fontfile=$SER:text='$T':fontsize=150:fontcolor=white:x=(w-tw)/2:y=405:shadowcolor=black@0.6:shadowx=3:shadowy=3,\
drawtext=fontfile=$SER:text='$Q':fontsize=52:fontcolor=0xE6E6E6:x=(w-tw)/2:y=615:shadowcolor=black@0.7:shadowx=2:shadowy=2,format=rgba" "$OUT"
