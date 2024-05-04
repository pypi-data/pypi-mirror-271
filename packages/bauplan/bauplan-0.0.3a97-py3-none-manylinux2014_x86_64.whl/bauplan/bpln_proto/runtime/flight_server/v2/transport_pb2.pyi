from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class FlightServerRequest(_message.Message):
    __slots__ = ('runner_instructions',)
    RUNNER_INSTRUCTIONS_FIELD_NUMBER: _ClassVar[int]
    runner_instructions: FlightServerRequestRunnerInstructions
    def __init__(
        self, runner_instructions: _Optional[_Union[FlightServerRequestRunnerInstructions, _Mapping]] = ...
    ) -> None: ...

class FlightServerRequestRunnerInstructions(_message.Message):
    __slots__ = (
        'models',
        'job_id',
        'physical_plan_id',
        'task_id',
        'flight_server_timeout',
        'enable_lz4_compression',
        'server_ip_addr',
        'server_ip_port',
    )
    MODELS_FIELD_NUMBER: _ClassVar[int]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_SERVER_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    ENABLE_LZ4_COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    SERVER_IP_ADDR_FIELD_NUMBER: _ClassVar[int]
    SERVER_IP_PORT_FIELD_NUMBER: _ClassVar[int]
    models: _containers.RepeatedCompositeFieldContainer[ArrowModel]
    job_id: str
    physical_plan_id: str
    task_id: str
    flight_server_timeout: int
    enable_lz4_compression: bool
    server_ip_addr: str
    server_ip_port: int
    def __init__(
        self,
        models: _Optional[_Iterable[_Union[ArrowModel, _Mapping]]] = ...,
        job_id: _Optional[str] = ...,
        physical_plan_id: _Optional[str] = ...,
        task_id: _Optional[str] = ...,
        flight_server_timeout: _Optional[int] = ...,
        enable_lz4_compression: bool = ...,
        server_ip_addr: _Optional[str] = ...,
        server_ip_port: _Optional[int] = ...,
    ) -> None: ...

class ArrowModel(_message.Message):
    __slots__ = ('id', 'parts')
    ID_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    parts: _containers.RepeatedCompositeFieldContainer[ModelPart]
    def __init__(
        self, id: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[ModelPart, _Mapping]]] = ...
    ) -> None: ...

class ModelPart(_message.Message):
    __slots__ = ('shmem_part', 'disk_part')
    SHMEM_PART_FIELD_NUMBER: _ClassVar[int]
    DISK_PART_FIELD_NUMBER: _ClassVar[int]
    shmem_part: ShmemPart
    disk_part: DiskPart
    def __init__(
        self,
        shmem_part: _Optional[_Union[ShmemPart, _Mapping]] = ...,
        disk_part: _Optional[_Union[DiskPart, _Mapping]] = ...,
    ) -> None: ...

class ShmemPart(_message.Message):
    __slots__ = ('shmem_key', 'part_id')
    SHMEM_KEY_FIELD_NUMBER: _ClassVar[int]
    PART_ID_FIELD_NUMBER: _ClassVar[int]
    shmem_key: str
    part_id: str
    def __init__(self, shmem_key: _Optional[str] = ..., part_id: _Optional[str] = ...) -> None: ...

class DiskPart(_message.Message):
    __slots__ = ('disk_filepath', 'part_id')
    DISK_FILEPATH_FIELD_NUMBER: _ClassVar[int]
    PART_ID_FIELD_NUMBER: _ClassVar[int]
    disk_filepath: str
    part_id: str
    def __init__(self, disk_filepath: _Optional[str] = ..., part_id: _Optional[str] = ...) -> None: ...
