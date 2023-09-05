#!/usr/bin/env bash

export TRANSFORMERS_CACHE=/var/tmp/hf/models
export HF_HOME=/var/tmp/hf/misc
export HF_DATASETS_CACHE=/var/tmp/hf/datasets
export SENTENCE_TRANSFORMERS_HOME=/var/tmp/hf/sentence

if [[ -d ./DB && -n "$(ls -A ./DB)" ]]; then 
  echo "start.sh: Chroma index exists. If you want to build a new index plese remove DB directory."
  python run_server.py
else
  echo "start.sh: Chroma index does not exist. Let's create it!"
  python ingest.py --device_type cpu && python run_server.py
fi

# python ingest.py --device_type cpu && uwsgi --ini ./deploy/uwsgi.ini