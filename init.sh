#!/usr/bin/env bash

DEPS_LIST=("python" "pip" "virtualenv" "docker-machine" "docker-compose" "docker")
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

if [ ! -f "requirements.txt" ]; then
  echo "python requirements file is missing"
  exit 1
fi

source ./.env

IS_RUN="$(docker-machine ls --filter "name=${MACHINE_NAME}" --filter "state=Running" -q)"
if [[ -n "${IS_RUN}" ]]; then
  echo "docker-machine ${MACHINE_NAME} already exist"
else
  docker-machine create "${MACHINE_NAME}"
  docker-machine ssh "${MACHINE_NAME}" 'sysctl -w vm.max_map_count=262144'
fi

eval "$(docker-machine env "${MACHINE_NAME}")"

docker-compose up -d

if [[ ! -d "venv" ]]; then
  virtualenv venv
fi

source ./venv/bin/activate || source ./venv/Scripts/activate

pip install -r requirements.txt
