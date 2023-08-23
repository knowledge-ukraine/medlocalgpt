#!/usr/bin/env bash

export TRANSFORMERS_CACHE=/var/tmp/hf/models
export HF_HOME=/var/tmp/hf/misc
export HF_DATASETS_CACHE=/var/tmp/hf/datasets
export SENTENCE_TRANSFORMERS_HOME=/var/tmp/hf/sentence

if [[ -d ./DB && -n "$(ls -A ./DB)" ]]; then 
  echo "start.sh: Chroma index exists."
  uwsgi --ini ./deploy/uwsgi.ini
else
  echo "start.sh: Chroma index does not exist. Let's create it!"
  python ingest.py --device_type cpu && uwsgi --ini ./deploy/uwsgi.ini
fi

# python ingest.py --device_type cpu && uwsgi --ini ./deploy/uwsgi.ini