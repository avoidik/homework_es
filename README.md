# ES

Sample Elasticsearch application in python

## Prerequisites

* docker
* docker-machine
* docker-compose
* python3.6 (pip, virtualenv)

## Workflow

1. `init.sh` - start docker-machine with elasticsearch, prepare virtualenv
1. `exec.sh` - run python
1. `restart.sh` - recreate container with elasticsearch (delete volumes)
1. `exec.sh` - run python
1. `cleanup.sh` - remove docker-machine with elasticsearch, clean virtualenv up

## Copyright

You may use my work or its parts as you wish, but only with proper credits to me like this:

Viacheslav - avoidik@gmail.com
