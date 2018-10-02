#!/usr/bin/env bash

DEPS_LIST=("python" "docker-machine" "docker")
for item in "${DEPS_LIST[@]}"; do
  if ! command -v "$item" &> /dev/null ; then
    echo "Error: required command '$item' was not found"
    exit 1
  fi
done

if [ ! -f ".env" ]; then
  echo "environment definition is missing"
  exit 1
fi

source ./.env

IS_RUN="$(docker-machine ls --filter "name=${MACHINE_NAME}" --filter "state=Running" -q)"
if [[ -n "${IS_RUN}" ]]; then
  ES_SERVER_ADDR="$(docker-machine ip "${MACHINE_NAME}")" ES_PASSWORD="$ES_PASSWORD" python main.py
fi
