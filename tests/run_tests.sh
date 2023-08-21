#!/bin/bash

source bin/activate
python3 -m pytest -v --no-header tests/test_forms.py | tee tests/results.txt
deactivate
