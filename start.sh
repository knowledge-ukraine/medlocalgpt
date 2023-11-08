#!/usr/bin/env bash

# export TRANSFORMERS_CACHE=/var/tmp/hf/models
# export HF_HOME=/var/tmp/hf/misc
# export HF_DATASETS_CACHE=/var/tmp/hf/datasets
# export SENTENCE_TRANSFORMERS_HOME=/var/tmp/hf/sentence

uwsgi --ini ./deploy/uwsgi.ini