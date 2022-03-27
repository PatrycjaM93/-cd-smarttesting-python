#!/bin/bash

set -o errexit

CURRENT_DIR=$(pwd)

# Port, na którym będzie uruchomiony stub naszych kontraktów
STUB_PORT="5001"

SC_CONTRACT_DOCKER_VERSION="2.2.4.RELEASE"
# Port na którym bedzie działać Stubrunner (w tym przykładzie nie ma szczególnego znaczenia)
STUBRUNNER_PORT="8083"
# Wskazujemy którego stuba chcemy użyć
STUBRUNNER_IDS="com.example:smarttesting:+:$STUB_PORT"

# Miejsce wskazujące output z Spring Cloud Contract (01_generate_stubs_with_scc.sh)
STUBS_LOCALATION="${CURRENT_DIR}/05-03-01-producer/spring-cloud-contract-output/"
# Ustawienie Stubrunnera, które powoduje że będzie korzystał ze stubów w plikach
STUBRUNNER_REPOSITORY_ROOT="stubs://file:///scc_output"

docker run --rm -e "STUBRUNNER_IDS=${STUBRUNNER_IDS}" \
  -e STUBRUNNER_REPOSITORY_ROOT=$STUBRUNNER_REPOSITORY_ROOT \
  -e STUBRUNNER_STUBS_MODE=LOCAL \
  -p "${STUBRUNNER_PORT}:${STUBRUNNER_PORT}" \
  -p "$STUB_PORT:$STUB_PORT"  \
  -v "$STUBS_LOCALATION:/scc_output:ro" \
springcloud/spring-cloud-contract-stub-runner:"${SC_CONTRACT_DOCKER_VERSION}"
