#!/bin/bash

if [ ! -e cert/cert.pem ]; then
    make certificate
fi
python -m pytest -v --cov-report term-missing --cov --cov-fail-under 80
