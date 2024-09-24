#!/bin/sh

. $(dirname $0)/config

docker build -t $DOCKER_IMAGE .

cp $PROTO_PATH/$PROTO_FILE .


$DOCKER_RUN $DOCKER_IMAGE protoc \
	--cpp_out=. \
	--grpc_out=. \
	--plugin=protoc-gen-grpc=/usr/bin/grpc_cpp_plugin \
	-I. \
	$PROTO_FILE

$DOCKER_RUN $DOCKER_IMAGE pip install setuptools

# build wheel package for python
$DOCKER_RUN $DOCKER_IMAGE python3 setup.py build bdist_wheel
