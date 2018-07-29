#!/bin/sh
cd /home/svasilovski/python/webServer/
clear
export FLASK_APP=wsAccionesDeUsuarioFlask.py
python -m flask run --host=0.0.0.0  --port=8000
