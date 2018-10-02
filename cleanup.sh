#!/usr/bin/env bash

if [[ -d "venv" ]]; then
  rm -rf ./venv
fi

DEPS_LIST=("docker-machine" "docker-compose" "docker")
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
  eval "$(docker-machine env "${MACHINE_NAME}")"
  docker-compose down -v
  docker-machine stop "${MACHINE_NAME}"
  docker-machine rm "${MACHINE_NAME}" -f -y
fi
