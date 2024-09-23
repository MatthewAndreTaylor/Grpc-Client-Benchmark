# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import image_service_pb2 as image__service__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in image_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ImageServiceStub(object):
    """Image service definition
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListImages = channel.unary_unary(
                '/image_service.ImageService/ListImages',
                request_serializer=image__service__pb2.ListImagesRequest.SerializeToString,
                response_deserializer=image__service__pb2.ListImagesResponse.FromString,
                _registered_method=True)
        self.StreamImages = channel.unary_stream(
                '/image_service.ImageService/StreamImages',
                request_serializer=image__service__pb2.StreamImagesRequest.SerializeToString,
                response_deserializer=image__service__pb2.StreamImagesResponse.FromString,
                _registered_method=True)


class ImageServiceServicer(object):
    """Image service definition
    """

    def ListImages(self, request, context):
        """List available image names
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamImages(self, request, context):
        """Stream images based on the provided names
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListImages': grpc.unary_unary_rpc_method_handler(
                    servicer.ListImages,
                    request_deserializer=image__service__pb2.ListImagesRequest.FromString,
                    response_serializer=image__service__pb2.ListImagesResponse.SerializeToString,
            ),
            'StreamImages': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamImages,
                    request_deserializer=image__service__pb2.StreamImagesRequest.FromString,
                    response_serializer=image__service__pb2.StreamImagesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'image_service.ImageService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('image_service.ImageService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ImageService(object):
    """Image service definition
    """

    @staticmethod
    def ListImages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/image_service.ImageService/ListImages',
            image__service__pb2.ListImagesRequest.SerializeToString,
            image__service__pb2.ListImagesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StreamImages(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/image_service.ImageService/StreamImages',
            image__service__pb2.StreamImagesRequest.SerializeToString,
            image__service__pb2.StreamImagesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
