#!/bin/bash
# usage: fetch.sh cache_dir url  -> saves to cache_dir/<md5>.html if missing
f=$1/$(printf %s "$2" | md5sum | cut -d' ' -f1).html; [ -s $f ] || curl -sSL -m 40 --retry 2 -o $f "$2"
