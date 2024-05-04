#!/bin/bash
python3 -m twine upload \
        --skip-existing \
        --config-file ./.pypirc \
        --repository testpypi \
        dist/*
