
set -o errexit
set -o errtrace
set -o pipefail

export CURL_BIN="${CURL_BIN:-curl}"
export URL="${URL:-https://reqres.in/api/users/2}"

request
