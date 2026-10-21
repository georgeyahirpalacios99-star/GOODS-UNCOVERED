#!/bin/bash
# Genera un PNG transparente 1920x1080 con un texto grande centrado y un subtitulo opcional (estilo Goods Uncovered)
# uso: tools/png_label.sh salida.png "TEXTO" ["subtitulo"] [white|amber|red] [tamaño]
set -e
SER=/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf
SANS=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
OUT="$1"; TXT="$2"; SUB="$3"; COL="${4:-white}"; SIZE="${5:-170}"
case "$COL" in amber) C=0xE8A33D;; red) C=0xD7263D;; *) C=white;; esac
esc(){ printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e "s/'/’/g" -e 's/:/\\:/g' -e 's/%/\\%/g'; }
F="drawtext=fontfile=$SER:text='$(esc "$TXT")':fontsize=$SIZE:fontcolor=$C:x=(w-tw)/2:y=(h-th)/2-30:shadowcolor=black@0.65:shadowx=4:shadowy=4"
[ -n "$SUB" ] && F="$F,drawtext=fontfile=$SANS:text='$(esc "$SUB")':fontsize=50:fontcolor=white@0.92:x=(w-tw)/2:y=h/2+$((SIZE/2+20)):shadowcolor=black@0.7:shadowx=2:shadowy=2"
ffmpeg -loglevel error -y -f lavfi -i "color=c=black@0.0:s=1920x1080,format=rgba" -frames:v 1 -vf "$F,format=rgba" "$OUT"
