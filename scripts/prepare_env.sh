#!/bin/bash


snap install --classic pre-commit
pip install --upgrade pre-commit==2.9.2

rm -r .env
virtualenv .env
source .env/bin/activate

pip install -r requirements.txt
pip install --upgrade pip
