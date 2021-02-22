#!/usr/bin/env sh

if [ "$1" != "" ] && [ "$1" != "test" ] && [ "$1" != "stop" ]; then
    >&2 printf "Bad argument %s.\n" "${1}"
    >&2 printf "Options:\n"
    >&2 printf "\t<no args>          -- Reads the sample config file and prints a beautified json version to stdout\n"
    >&2 printf "\t<stop>             -- Removes container and network\n"
    >&2 printf "\t<test>             -- Run tests on the config parser\n"
    exit 1;
fi

NET=$(docker network ls -q --filter name=sec-net)
CONTAINER=$(docker ps -a -q --filter name="config_parser" --format="{{.ID}}")
IMAGE=$(docker images -q python:3.8.7-alpine3.12)


if [ "$1" = "stop" ]; then
  docker rm -f "$CONTAINER" > /dev/null 2>&1
  docker network rm "$NET" > /dev/null 2>&1
  docker rmi "$IMAGE" > /dev/null 2>&1
else
  if [ "$1" = "test" ]; then
    COMMAND="python tests.py"
  else
    COMMAND=$'python -c "$(cat <<- EOF
import app; app.parse_config(\'/usr/local/config.sample\')

EOF
    )"'
  fi
  if [ -z "$NET" ]; then
    docker network create sec-net
  fi
  docker run \
    -t \
    -v "$(pwd)/src:/usr/local/parser" \
    -v "$(pwd)/config.sample:/usr/local/config.sample" \
    -w /usr/local/parser \
    --rm \
    --name config_parser \
    --network sec-net \
    python:3.8.7-alpine3.12 \
    /bin/ash -c "$COMMAND"
fi
