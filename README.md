# Example multiprocess gRPC server

### Create pb2 from proto

```bash
python -m grpc_tools.protoc -I./protos --python_out=./ --grpc_python_out=./ --mypy_out=./ ./protos/example.proto
```

### Start

```bash
docker-compose up --build -d
```

### Stop

```bash
docker-compose down
```


### Request

```bash
python client.py
```
