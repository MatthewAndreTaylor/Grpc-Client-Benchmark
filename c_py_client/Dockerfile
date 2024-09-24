FROM ubuntu:latest

RUN apt update && apt install -y \
	python3-full \
	python3-pip \
	autoconf \
	build-essential \
	libgrpc++-dev \
	libprotobuf-dev \
	libtool \
	pkg-config \
	protobuf-compiler \
	protobuf-compiler-grpc \
	&& apt clean \
	&& rm -rf /var/lib/apt/lists/*