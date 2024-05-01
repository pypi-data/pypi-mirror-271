from google.protobuf import empty_pb2 as _empty_pb2
from fintekkers.requests.util.lock import lock_request_pb2 as _lock_request_pb2
from fintekkers.requests.util.lock import lock_response_pb2 as _lock_response_pb2
from fintekkers.models.util.lock import node_partition_pb2 as _node_partition_pb2
from fintekkers.models.util.lock import node_state_pb2 as _node_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NamespaceList(_message.Message):
    __slots__ = ["namespaces"]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    namespaces: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespaces: _Optional[_Iterable[str]] = ...) -> None: ...

class NodeStateList(_message.Message):
    __slots__ = ["nodes"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_node_state_pb2.NodeState]
    def __init__(self, nodes: _Optional[_Iterable[_Union[_node_state_pb2.NodeState, _Mapping]]] = ...) -> None: ...

class PartitionsList(_message.Message):
    __slots__ = ["partitions"]
    PARTITIONS_FIELD_NUMBER: _ClassVar[int]
    partitions: _containers.RepeatedCompositeFieldContainer[_node_partition_pb2.NodePartition]
    def __init__(self, partitions: _Optional[_Iterable[_Union[_node_partition_pb2.NodePartition, _Mapping]]] = ...) -> None: ...
