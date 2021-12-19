#!/usr/bin/env bash

# This script builds Docker container and pushes it to ECR,

# Usage examples:
# "sh build_and_push.sh"

image="hackathon-mirage-8"
tag="latest"
dockerfile="."
fullname="174466744028.dkr.ecr.ap-southeast-1.amazonaws.com/hackathon-mirage-8"

# Get the login command from ECR and execute it directly
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin 174466744028.dkr.ecr.ap-southeast-1.amazonaws.com

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build -t ${image} .
docker tag ${image} ${fullname}
docker push ${fullname}