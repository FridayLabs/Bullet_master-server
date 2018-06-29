#!/bin/bash

if [ ! -e cert/cert.pem ]; then
    make certificate
fi

if [ -d "tests-reports" ]; then
    python -m pytest -v --cov-report term-missing --cov --cov-fail-under 80 --junitxml=test-reports/junit.xml
else
    python -m pytest -v --cov-report term-missing --cov --cov-fail-under 80
fi
