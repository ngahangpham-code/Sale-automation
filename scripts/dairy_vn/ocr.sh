#!/bin/bash
# usage: ocr.sh file.pdf -> file.ocr.txt ; first 4 pages, longest side 2400px, 90s/page cap
f=$1; b=${f%.pdf}; [ -s $b.ocr.txt ] && exit 0
d=$(mktemp -d); timeout 120 pdftoppm -l 4 -gray -scale-to 2400 $f $d/p >/dev/null 2>&1
for p in $d/p*; do OMP_THREAD_LIMIT=1 timeout 90 tesseract $p - -l vie --psm 4 2>/dev/null; done > $b.ocr.txt; rm -rf $d
