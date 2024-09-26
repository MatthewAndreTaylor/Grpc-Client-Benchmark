# Comparing grpc python client library performance

This library intends to bench mark the performance of streaming images using grpc to python clients.
The service implements two endpoints

- `/ListImages` => returns the names of the images the server can stream
- `/StreamImages` => returns a stream of images given requested image names

Set up test server

```
cd test-server

./build

./run
```

Run the python client profiler

```
poetry install

poetry run python grpc_python_profile.py 
```

This will compile a graph inside the `_profiles` directory


<img src="https://github.com/MatthewAndreTaylor/protoWrap/blob/main/_profiles/grpc_python_profile-46.png" />
