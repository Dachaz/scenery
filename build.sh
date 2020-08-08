#!/bin/bash

# Python 2 build
docker build -t scenery-py2 -f py2.Dockerfile .
docker run scenery-py2

# Python 3 build
docker build -t scenery-py3 -f py3.Dockerfile .
docker run scenery-py3
