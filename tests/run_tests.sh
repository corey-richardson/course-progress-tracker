#!/bin/bash

source bin/activate
python3 -m pytest -v tests/test_forms.py > tests/results.txt
deactivate