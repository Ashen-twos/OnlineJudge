#!/bin/bash

set -xe

Version=$1
ImageId=`docker images | grep backend | grep ${Version} | grep -v /backend | awk '{print $3}'`

docker login --username=ashentoo registry.cn-hangzhou.aliyuncs.com -p a1806996288
docker tag ${ImageId} registry.cn-hangzhou.aliyuncs.com/ashentoo/backend:${Version}
docker push registry.cn-hangzhou.aliyuncs.com/ashentoo/backend:${Version}