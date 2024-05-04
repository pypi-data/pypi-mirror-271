# This Python module provides functionality to generate typed stubs for the generated gRPC code.
# The gRPC code, which can be used both synchronously and asynchronously, requires the stubs
# to be cast into the proper type to ensure correct typing.

from typing import TYPE_CHECKING, cast, overload

import grpc
import grpc.aio

from fundamentum_edge_proto.configuration_pb2_grpc import ConfigurationStub
from fundamentum_edge_proto.provisioning_pb2_grpc import ProvisioningStub
from fundamentum_edge_proto.states_pb2_grpc import StatesEventStub
from fundamentum_edge_proto.telemetry_pb2_grpc import TelemetryStub

if TYPE_CHECKING:
    from fundamentum_edge_proto.configuration_pb2_grpc import ConfigurationAsyncStub
    from fundamentum_edge_proto.provisioning_pb2_grpc import ProvisioningAsyncStub
    from fundamentum_edge_proto.states_pb2_grpc import StatesEventAsyncStub
    from fundamentum_edge_proto.telemetry_pb2_grpc import TelemetryAsyncStub


@overload
def build_configuration_stub(channel: grpc.Channel) -> ConfigurationStub: ...
@overload
def build_configuration_stub(channel: grpc.aio.Channel) -> "ConfigurationAsyncStub": ...
def build_configuration_stub(channel):
    stub = ConfigurationStub(channel)
    if isinstance(channel, grpc.aio.Channel):
        return cast("ConfigurationAsyncStub", stub)
    return stub


@overload
def build_provisioning_stub(channel: grpc.Channel) -> ProvisioningStub: ...
@overload
def build_provisioning_stub(channel: grpc.aio.Channel) -> "ProvisioningAsyncStub": ...
def build_provisioning_stub(channel):
    stub = ProvisioningStub(channel)
    if isinstance(channel, grpc.aio.Channel):
        return cast("ProvisioningAsyncStub", stub)
    return stub


@overload
def build_states_event_stub(channel: grpc.Channel) -> StatesEventStub: ...
@overload
def build_states_event_stub(channel: grpc.aio.Channel) -> "StatesEventAsyncStub": ...
def build_states_event_stub(channel):
    stub = StatesEventStub(channel)
    if isinstance(channel, grpc.aio.Channel):
        return cast("StatesEventAsyncStub", stub)
    return stub


@overload
def build_telemetry_stub(channel: grpc.Channel) -> TelemetryStub: ...
@overload
def build_telemetry_stub(channel: grpc.aio.Channel) -> "TelemetryAsyncStub": ...
def build_telemetry_stub(channel):
    stub = TelemetryStub(channel)
    if isinstance(channel, grpc.aio.Channel):
        return cast("TelemetryAsyncStub", stub)
    return stub
