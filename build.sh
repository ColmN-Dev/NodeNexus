#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

python -m pip install -r backend/requirements.txt
python backend/manage.py migrate --noinput
python backend/manage.py collectstatic --noinput