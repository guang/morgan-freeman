#!/bin/bash
# tag=0.1.0
tag=latest
set -e
docker build -t guangyang/morgan-freeman:${tag} .
docker push guangyang/morgan-freeman:${tag}
