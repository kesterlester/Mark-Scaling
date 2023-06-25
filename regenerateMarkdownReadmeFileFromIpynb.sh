#!/bin/sh

python3 -m venv venv ; pip install --upgrade pip ; pip install notebook matplotlib ; source venv/bin/activate

jupyter nbconvert --execute --to markdown README.ipynb 

