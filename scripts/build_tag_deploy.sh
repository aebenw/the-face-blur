#!/usr/bin/env bash
set -x

if [ -z "$1" ]
then
    TAG="latest"
else
    TAG=$1
fi

echo "Building version: $TAG of faceoff."

docker build -t faceoff:$TAG  -f Dockerfile .
eval $(aws ecr get-login --no-include-email --region us-east-1 | sed 's|-e none||' | sed 's|https://||')
docker tag faceoff:$TAG 601654182899.dkr.ecr.us-east-1.amazonaws.com/faceoff:$TAG
docker push 601654182899.dkr.ecr.us-east-1.amazonaws.com/faceoff

if [ $? -eq 0 ]; then
    echo "faceoff:$TAG published OK!"
else
    echo "faceoff:$TAG failed push to ECR"
fi
