#!/bin/sh

[ -f /tmp/debug_apkg ] && echo "APKG_DEBUG: $0 $@" >> /tmp/debug_apkg

path=$1

#link binary
ln -sf $path/app/scenery-bin /usr/sbin/scenery

WEBPATH="/var/www/scenery/"
mkdir -p $WEBPATH

ln -sf $path/web/* $WEBPATH
