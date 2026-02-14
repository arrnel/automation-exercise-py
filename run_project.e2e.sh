#!/bin/bash

set -euo pipefail
source ./docker.properties
# -------------------------
# Configs
# -------------------------
export TEST_IMAGE_NAME="automation-exercise-tests"
export SELENOID_COMPOSE_FILE="docker-compose.yaml"
export BROWSERS_JSON_FILE="./env/docker/selenoid/local/browsers.json"
export BROWSER_CHANNEL="stable"
export PREFIX=${IMAGE_PREFIX}
export ALLURE_DIR="./allure-results"
export ARCH=$(uname -m)

function pull_browsers_from_browser_json() {

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

}

function pull_browser_from_env_variables {
  IS_NEW_BROWSER=false
  if [ "$BROWSER_NAME" == "chrome" ]; then
      awk "BEGIN {exit !($BROWSER_VERSION > 128.0)}" && IS_NEW_BROWSER=true
  elif [ "$BROWSER_NAME" == "firefox" ]; then
      awk "BEGIN {exit !($BROWSER_VERSION > 125.0)}" && IS_NEW_BROWSER=true
  fi

  if [ "$IS_NEW_BROWSER" == "true" ]; then
      VERSION="${BROWSER_VERSION%%.*}"
      BROWSER_IMAGE="twilio/selenoid:${BROWSER_NAME}_${BROWSER_CHANNEL}_${VERSION}"
  else
      BROWSER_IMAGE="selenoid/vnc_${BROWSER_NAME}:${BROWSER_VERSION}"
  fi

  echo "### Pull browser image: $BROWSER_IMAGE"
  docker pull $BROWSER_IMAGE

}

function pull_video_recorder() {
  if [ "$BROWSER_REMOTE_VIDEO" -ne "false"]; then
    echo "### Pull selenoid/video-recorder:latest-release"
    docker pull selenoid/video-recorder:latest-release
  else
    echo "Skip pulling selenoid video recorder"
  fi
}

function pull_browser() {
  if [ -z "$BROWSER_NAME" ] && [ -z "$BROWSER_VERSION" ]; then
    pull_browsers_from_browser_json
  else
    pull_browser_from_env_variables
  fi
}

# --------------------------------------------------------
# Step 0: Remove allure-results dir
# --------------------------------------------------------
echo "### Clear allure-results dir ###"
rm -rf $ALLURE_DIR
mkdir $ALLURE_DIR

# --------------------------------------------------------
# Step 1: Check all browsers in browsers.json exists
# --------------------------------------------------------
pull_browser
pull_video_recorder

# --------------------------------------------------------
# Step 2: Cleanup previous run
# --------------------------------------------------------
echo "### Stopping all services ###"
docker compose -f $SELENOID_COMPOSE_FILE down
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