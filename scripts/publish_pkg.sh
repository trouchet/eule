#!/bin/bash

bash scripts/prepare_env.sh
python setup.py sdist bdist_wheel
twine upload --skip-existing dist/*

