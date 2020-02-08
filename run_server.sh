#!/bin/bash

HOST=0.0.0.0
PORT=8000

export FLASK_APP=apps
export FLASK_ENV=debug
rm -rf apps.egg-info
pip install -e .

flask run -h ${HOST} -p ${PORT} --with-threads --reload --debugger