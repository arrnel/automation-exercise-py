#!/bin/bash

set -e

# -------------------------
# Configs
# -------------------------
export TEST_IMAGE_NAME="automation-exercise"
export SELENOID_COMPOSE_FILE="docker-compose.yml"
export BROWSERS_JSON_FILE="${TEST_IMAGE_NAME}/env/docker/selenoid/browsers.json"
export ALLURE_DIR="${TEST_IMAGE_NAME}/allure-results"
# --------------------------------------------------------
# Step 1: Check all browsers in browsers.json exists
# --------------------------------------------------------
if [ -f "$BROWSERS_JSON_FILE" ]; then
  BROWSERS=$(grep -o '"image": "[^"]*' "$BROWSERS_JSON_FILE" | awk -F': "' '{print $2}')

  for IMAGE in $BROWSERS; do
    if [[ "$(docker images -q $IMAGE 2> /dev/null)" == "" ]]; then
      echo "Downloading $IMAGE..."
      docker pull $IMAGE
    else
      echo "$IMAGE already exists."
    fi
  done
else
  echo "browsers.json not found! Skipping browser download."
fi

# --------------------------------------------------------
# Step 2: Building tests image
# --------------------------------------------------------
SKIP_BUILD=false
for arg in "$@"; do
  if [[ "$arg" == "--skip-build" ]]; then
    SKIP_BUILD=true
  fi
done

if [ "$SKIP_BUILD" = false ]; then
  docker compose down
  DOCKER_CONTAINERS=$(docker ps -a -q)

  if [ -n "$DOCKER_CONTAINERS" ]; then
    docker stop $DOCKER_CONTAINERS
    echo "### Removing containers: $DOCKER_CONTAINERS ###"
    docker rm $DOCKER_CONTAINERS
  fi

  DOCKER_IMAGES=$(docker images --format '{{.Repository}}:{{.Tag}}' | grep "$TEST_IMAGE_NAME")
  if [ -n "$DOCKER_IMAGES" ]; then
    echo "### Removing images: $DOCKER_IMAGES ###"
    docker rmi $DOCKER_IMAGES
  fi

else
  echo "Skip build test image (--skip-build)."
  docker compose rm -f $TEST_IMAGE_NAME
fi

echo "### Running test image build ###"
docker compose -f $SELENOID_COMPOSE_FILE up -d $TEST_IMAGE_NAME

# -------------------------
# Step 3: Show running containers
# -------------------------
docker -ps a
