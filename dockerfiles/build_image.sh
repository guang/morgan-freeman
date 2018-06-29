#!/bin/bash
# tag=0.1.0
tag=latest
set -e
docker build -t guangyang/morgan-freeman:${tag} -f Dockerfile .
docker push guangyang/morgan-freeman:${tag}


docker build -t guangyang/morgan-freeman-cpu:${tag} -f Dockerfile.cpu .
docker push guangyang/morgan-freeman-cpu:${tag}
