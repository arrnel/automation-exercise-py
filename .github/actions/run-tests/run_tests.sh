#!/usr/bin/env bash
set -euo pipefail

SHOW_LOGS="$1"
REMOVE_COMPOSE_DATA="$2"
PREFIX="$3"

docker compose -f docker-compose.ci.yaml up -d
docker ps -a
docker wait automation-exercise-tests

if [ "$SHOW_LOGS" = "true" ]; then
  echo "### Test logs ###"
  docker logs automation-exercise-tests
fi

if [ "$REMOVE_COMPOSE_DATA" = "true" ]; then

  echo "### Close and remove compose containers ###"
  docker compose rm -sf

  echo "### Remove test container image $PREFIX/automation-exercise-tests:latest"
  docker image rm $PREFIX/automation-exercise-tests:latest

fi