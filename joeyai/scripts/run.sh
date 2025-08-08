#!/bin/bash
source .venv/bin/activate
export FLASK_APP=joeyai/backend/app.py
flask run --port=5000
