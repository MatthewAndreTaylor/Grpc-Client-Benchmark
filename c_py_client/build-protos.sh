#!/bin/bash


_pcb_dir=$(dirname "${BASH_SOURCE[0]}")

_CLIENT_ROOT=$(realpath "${_pcb_dir}")

build-client()
{
    local files
    local files_array

    pushd ${_CLIENT_ROOT} > /dev/null

    # /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # test -d ~/.linuxbrew && eval "$(~/.linuxbrew/bin/brew shellenv)"
    # test -d /home/linuxbrew/.linuxbrew && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
    # echo "eval \"\$($(brew --prefix)/bin/brew shellenv)\"" >> ~/.bashrc

    brew install grpc
    brew install protobuf

    export PATH="/usr/local/opt/protobuf/bin:$PATH"

    which grpc_cpp_plugin   # >> /home/linuxbrew/.linuxbrew/bin/grpc_cpp_plugin

    proto_folder="${_CLIENT_ROOT}/../"
    files=$(find "$proto_folder" -name '*.proto')
    IFS=$'\n' read -r -d '' -a files_array <<< "$files"

    echo files_array: "${files_array[@]}"

    protoc -I"$proto_folder" \
           --cpp_out="${_CLIENT_ROOT}" \
           --grpc_out="${_CLIENT_ROOT}" \
           --plugin=protoc-gen-grpc=$(which grpc_cpp_plugin) \
           "${files_array[@]}"


    popd > /dev/null

    return $?
}

build-client "$@"