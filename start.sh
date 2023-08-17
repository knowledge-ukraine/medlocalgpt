#!/usr/bin/env bash

python ingest.py --device_type cpu

uwsgi --ini ./deploy/uwsgi.ini