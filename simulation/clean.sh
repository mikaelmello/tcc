#!/bin/sh

find . -type d -regex "./src/runners/java/.*/target" -exec rm -rf {} \;
find . -type d -regex "./src/runners/python/.*/venv" -exec rm -rf {} \;

