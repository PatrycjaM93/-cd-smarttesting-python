#!/bin/bash
SC_CONTRACT_DOCKER_VERSION="2.2.4.RELEASE"

PROJECT_NAME="smarttesting"
PROJECT_VERSION="0.0.1.RELEASE"

NETWORKING=""
SYSTEM_NAME=$(uname -s)
if [ "$SYSTEM_NAME" == "Linux" ]
then
  APPLICATION_BASE_URL="http://localhost:5000"
  # to nie działa na Macu, a Sprint Cloud Contracts musi dobić się do aplikacji
  NETWORKING="--network host"
else
  # Windows & MacOS
  APPLICATION_BASE_URL="http://host.docker.internal:5000"
fi

CURRENT_DIR=$(pwd)

# Wygenerowane pliki stubów znajdziemy w folderze producenta/spring-cloud-contract-output/
docker run  --rm $NETWORKING \
  -e "APPLICATION_BASE_URL=${APPLICATION_BASE_URL}" \
  -e "PUBLISH_ARTIFACTS=false" \
  -e "PROJECT_NAME=${PROJECT_NAME}" \
  -e "PROJECT_VERSION=${PROJECT_VERSION}" \
  -v "${CURRENT_DIR}/05-03-01-producer/contracts/:/contracts:ro" \
  -v "${CURRENT_DIR}/05-03-01-producer/spring-cloud-contract-output:/spring-cloud-contract-output/" \
  springcloud/spring-cloud-contract:"${SC_CONTRACT_DOCKER_VERSION}"
