#!/bin/bash

source bin/activate
python3 -m pytest -v --no-header | tee tests/results.txt
deactivate
