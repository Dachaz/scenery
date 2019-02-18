#!/bin/bash

# Switch to the directory where build.sh is
cd "${0%/*}"
# Put the wdc binaries next to pyb binaries
mkdir -p ${PWD}/../target/wdc
# Copy the latest scenery code into the wdc app folder
rsync -rav --exclude=.DS_Store --exclude='*.pyc' ../src/scenery src/app
# Build using docker
docker build -t scenery-wdc .
docker run -i -v ${PWD}/../target/wdc:/build scenery-wdc
# Remove the copied code
rm -rf ./src/app/scenery/
