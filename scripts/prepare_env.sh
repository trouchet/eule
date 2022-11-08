#!/bin/bash

activate () {
  . ../.env/bin/activate
}

snap install --classic pre-commit
pip install --upgrade pre-commit==2.9.2
virtualenv ./.env
activate
pip install -r requirements_dev.txt
pip install --upgrade pip
