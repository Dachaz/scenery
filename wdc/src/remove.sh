#!/bin/sh

[ -f /tmp/debug_apkg ] && echo "APKG_DEBUG: $0 $@" >> /tmp/debug_apkg

APKG_PATH=$1
WEBPATH="/var/www/scenery"

rm -rf $APKG_PATH
rm -rf $WEBPATH
