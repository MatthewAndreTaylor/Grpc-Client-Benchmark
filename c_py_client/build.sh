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

# Create a virtual environment inside Docker container
$DOCKER_RUN $DOCKER_IMAGE python3 -m venv .venv

# Activate the virtual environment and install setuptools and wheel
$DOCKER_RUN $DOCKER_IMAGE .venv/bin/pip install setuptools wheel

# Install the current package inside the virtual environment
$DOCKER_RUN $DOCKER_IMAGE .venv/bin/python3 setup.py install

# Run the client
$DOCKER_RUN $DOCKER_IMAGE .venv/bin/python3 client.py
