# Comparing grpc python client library performance


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
