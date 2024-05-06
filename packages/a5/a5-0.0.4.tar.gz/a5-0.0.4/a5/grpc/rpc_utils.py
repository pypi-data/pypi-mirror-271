import functools
from urllib.parse import urlparse

import grpc
from google.protobuf import descriptor, descriptor_pb2, descriptor_pool, message_factory


class CookieAuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, cookie):
        self._cookie = cookie

    def __call__(self, context, callback):
        callback((("cookie", f"couchers-sesh={self._cookie}"),), None)


def construct_creds_and_address(grpc_path, key=None):
    """
    Parses grpc paths, examples:

    * "tls://:api_key@example.com:8443"
    * "local://localhost:8888"
    * "tls://noauth.example.com:8443"

    Allows passing an extra key in case that is more dynamic
    """
    p = urlparse(grpc_path)

    if p.scheme == "tls":
        creds = grpc.ssl_channel_credentials()
    elif p.scheme == "local":
        creds = grpc.local_channel_credentials()
    else:
        raise ValueError(f"Don't know how to handle {p.scheme=}")

    key_ = p.password or key
    if key_:
        creds = grpc.composite_channel_credentials(creds, grpc.metadata_call_credentials(CookieAuthPlugin(key_)))

    return f"{p.hostname}:{p.port}", creds


def make_class(descriptor_: descriptor_pb2.DescriptorProto):
    """
    note that protobuf will be unhappy if you call this with the same descriptor twice
    """
    return message_factory.GetMessageClass(descriptor.MakeDescriptor(descriptor_))


@functools.lru_cache(maxsize=None)
def get_descriptor_data(descriptors_pb: bytes):
    """
    Generates a protocol buffer object descriptor pool which allows looking up info about our proto API, such as options
    for each servicer, method, or message.
    """
    pool = descriptor_pool.DescriptorPool()
    desc = descriptor_pb2.FileDescriptorSet.FromString(descriptors_pb)
    for file_descriptor in desc.file:
        pool.Add(file_descriptor)
    files = [f.name for f in desc.file]
    return pool, files, message_factory.GetMessageClassesForFiles(files, pool)


@functools.lru_cache(maxsize=None)
def _make_empty_httpbody():
    """
    caching is not for caching but to make sure we don't generate the classes twice
    """
    Empty = make_class(descriptor_pb2.DescriptorProto(name="_Empty"))
    HttpBody = make_class(
        descriptor_pb2.DescriptorProto(
            name="_HttpBody",
            field=[
                descriptor_pb2.FieldDescriptorProto(
                    name="content_type",
                    number=1,
                    type=descriptor_pb2.FieldDescriptorProto.Type.TYPE_STRING,
                ),
                descriptor_pb2.FieldDescriptorProto(
                    name="data",
                    number=2,
                    type=descriptor_pb2.FieldDescriptorProto.Type.TYPE_BYTES,
                ),
            ],
        )
    )
    return Empty, HttpBody


def _fetch_couchers_descriptors(grpc_path):
    Empty, HttpBody = _make_empty_httpbody()
    with grpc.secure_channel(*construct_creds_and_address(grpc_path)) as c:
        func = c.unary_unary(
            f"/org.couchers.bugs.Bugs/GetDescriptors",
            Empty.SerializeToString,
            HttpBody.FromString,
        )
        return func(Empty()).data


@functools.lru_cache(maxsize=None)
def get_couchers_descriptor_data(grpc_path):
    return get_descriptor_data(_fetch_couchers_descriptors(grpc_path))
