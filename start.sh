#!/bin/bash

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# Find all subdirectories containing a docker-compose.yml file
subfolders=$(find . -type f -name "docker-compose.yml" -exec dirname {} \;)

# Iterate over each subfolder and start docker-compose
for folder in $subfolders; do
    echo "Starting docker-compose in $folder"
    (cd "$folder" && docker-compose up -d)
done



