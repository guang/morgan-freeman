#!/bin/bash
# tag=0.1.0
tag=latest
set -e
docker build -t guangyang/snapi:${tag} .
docker push guangyang/snapi:${tag}
