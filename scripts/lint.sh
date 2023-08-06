#!/usr/bin/env bash

set -e
set -x

mypy app
ruff app tests scripts
black app tests --check
isort app tests scripts --check-only
