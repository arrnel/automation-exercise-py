#!/bin/bash

set -e
source ./docker.properties
# -------------------------
# Configs
# -------------------------
export TEST_IMAGE_NAME="automation-exercise-tests"
export SELENOID_COMPOSE_FILE="docker-compose.yaml"
export BROWSERS_JSON_FILE="./env/docker/selenoid/browsers.json"
export PREFIX=${IMAGE_PREFIX}
export ALLURE_DIR="./allure-results"
export ARCH=$(uname -m)

# --------------------------------------------------------
# Step 0: Remove allure-results dir
# --------------------------------------------------------
echo "### Remove allure-results dir ###"
rm -rf $ALLURE_DIR

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
# Step 2: Cleanup previous run
# --------------------------------------------------------
echo "### Stopping all services ###"
docker compose -f $SELENOID_COMPOSE_FILE down

# Удаляем сервисы/контейнеры (опционально, по сервису)
docker compose -f $SELENOID_COMPOSE_FILE rm -f $TEST_IMAGE_NAME || true

# --------------------------------------------------------
# Step 3: Check and remove test images
# --------------------------------------------------------
echo "### Checking for existing test images ###"
FULL_IMAGE_NAME="${PREFIX:+$PREFIX/}$TEST_IMAGE_NAME"
echo "### Searching images with: docker images --format '{{.Repository}}:{{.Tag}}' | grep \"$FULL_IMAGE_NAME\" ###"

test_images=$(docker images --format '{{.Repository}}:{{.Tag}}' | grep "$FULL_IMAGE_NAME" ) || {
  echo "### ERROR: Failed to list Docker images! Check 'docker images' manually. ###"
  echo "### Continuing without removing test images ###"
  test_images=""
}

if [ -n "$test_images" ]; then
  echo "### Found test images: ###"
  echo "$test_images"
  echo "### Removing test images ###"
  docker rmi $test_images || echo "### Some images could not be removed (in use?). Skipping. ###"
else
  echo "### No test images with name containing '$FULL_IMAGE_NAME' found. Skipping removal. ###"
fi

# --------------------------------------------------------
# Step 4: Start all containers with rebuild
# --------------------------------------------------------
echo "### Building and starting all containers ###"
docker compose -f $SELENOID_COMPOSE_FILE up -d  --build # --build заставит пересобрать образ тестов

# -------------------------
# Step 5: Show running containers
# -------------------------
echo "### Running containers ###"
docker ps -a