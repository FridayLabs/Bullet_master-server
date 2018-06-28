#!/bin/bash

make certificate-dev
python -m pytest -v --cov-report term-missing --cov --cov-fail-under 80
