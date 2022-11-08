#!/bin/bash

activate () {
  . ../.env/bin/activate
}

virtualenv ./.env
activate
pip install -r requirements_dev.txt
pip install --upgrade pip