#!/bin/bash

poetry run black --check . && poetry run flake8 . && poetry run pytest tests
