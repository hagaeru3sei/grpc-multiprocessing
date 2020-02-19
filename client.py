import grpc
import example_pb2
import example_pb2_grpc


def main():
    proxy_channel = grpc.insecure_channel("localhost:80")
    channel1 = grpc.insecure_channel("localhost:50051")
    channel2 = grpc.insecure_channel("localhost:50052")
    channel3 = grpc.insecure_channel("localhost:50053")
    channel4 = grpc.insecure_channel("localhost:50054")
    stub = example_pb2_grpc.ExampleServiceStub(proxy_channel)
    request = example_pb2.Request(message="test")
    print("request: {}".format(request))
    reply = stub.ExampleServer(request)
    print("reply: {}".format(reply))


if __name__ == "__main__":
    main()
