#!/bin/bash
# Usage: bash -x run.sh [image name] [container name] [docker command e.g., "sudo docker"]

image_name="${1:-myimage}"
container_name="${2:-mycontainer}"
docker_command="${3:-docker}"

set +e  # Don't stop on error
${docker_command} stop ${container_name}
${docker_command} rm ${container_name}
${docker_command} image rm ${image_name}
set -e  # Stop on error

${docker_command} build --no-cache -t ${image_name} .
${docker_command} run -d --name ${container_name} -p 9990:80 ${image_name}
