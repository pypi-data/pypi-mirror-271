from typing import Optional, List, TypeVar, Generic, Dict

from pydantic import Field, BaseModel

from drax_sdk.model.dynamic import Value
from drax_sdk.model.node import State


T = TypeVar("T")


class PagedResult(BaseModel, Generic[T]):
    results: List[T] = []
    total_rows: int = Field(alias="totalRows")

    class Config:
        populate_by_name = True


class HandshakeRequest(BaseModel):
    node_id: int = Field(alias="nodeId")
    name: str
    association_code: str = Field(alias="associationCode")
    urn: str
    project_id: str = Field(alias="projectId")
    supported_types: List[str] = Field(alias="supportedTypes")
    configuration_publish_topic: str = Field(alias="configurationPublishTopic")
    state_publish_topic: str = Field(alias="statePublishTopic")
    initial_state: State = Field(alias="initialState")
    extras: List[Value]

    class Config:
        populate_by_name = True


class HandshakeResponse(BaseModel):
    node_id: int = Field(alias="nodeId")
    urn: str
    public_key: bytes = Field(alias="publicKey")
    private_key: bytes = Field(alias="privateKey")

    class Config:
        populate_by_name = True


class AssociationRequest(BaseModel):
    apiKey: str
    apiSecret: str
    associationCode: str
    urn: str


class ConfigurationRequest(BaseModel):
    api_key: str = Field(alias="apiKey", default=None)
    api_secret: str = Field(alias="apiSecret", default=None)
    node_id: Optional[int] = Field(alias="nodeId", default=None)
    urn: str = None
    codec: str = None
    cryptography_disabled: bool = Field(alias="cryptographyDisabled", default=False)
    timestamp: int = None
    configuration: Dict[str, str]

    @classmethod
    def from_configuration(cls, configuration):
        return cls(
            node_id=configuration.node_id,
            timestamp=configuration.timestamp,
            configuration=configuration.to_map(),
        )

    class Config:
        populate_by_name = True


class ConfigurationResponse(BaseModel):
    node_id: str = Field(alias="nodeId")
    timestamp: int = Field(alias="timestamp")
    urn: str | None = Field(alias="urn", default=None)
    configuration: bytes = Field(alias="configuration")
    cryptography_disabled: bool = Field(alias="cryptographyDisabled", default=False)

    class Config:
        populate_by_name = True


class StateRequest(BaseModel):
    api_key: str = Field(alias="apiKey", default=None)
    api_secret: str = Field(alias="apiSecret", default=None)
    node_id: Optional[str] = Field(alias="nodeId", default=None)
    urn: Optional[str] = None
    timestamp: int = None
    state: bytes
    codec: str = None
    cryptography_disabled: bool = Field(alias="cryptographyDisabled", default=False)

    class Config:
        populate_by_name = True


class StateResponse(BaseModel):
    node_id: Optional[str] = Field(alias="nodeId")
    urn: Optional[str] = None
    timestamp: int
    state: Dict[str, str]

    @classmethod
    def from_node_and_entry(cls, node, state):
        return cls(
            nodeId=node.id,
            urn=node.urn,
            timestamp=state.timestamp,
            state=state.to_map(),
        )

    @classmethod
    def from_state(cls, state):
        return cls(nodeId=state.nodeId, timestamp=state.timestamp, state=state.to_map())


class AuthenticationRequest(BaseModel):
    api_key: str = Field(alias="apiKey")
    api_secret: str = Field(alias="apiSecret")

    class Config:
        populate_by_name = True


class FindNodeByIdsRequest(BaseModel):
    node_ids: List[int] = Field(alias="nodeIds")

    class Config:
        populate_by_name = True


from pydantic import BaseModel, Field
from typing import Optional


class InstalledNode(BaseModel):
    id: str
    urn: str
    public_key: Optional[bytes] = Field(None, alias="publicKey")
    private_key: Optional[bytes] = Field(None, alias="privateKey")

    @property
    def public_key_hex(self) -> str:
        if self.public_key is None:
            return ""
        return self.public_key.hex()

    @property
    def private_key_hex(self) -> str:
        if self.private_key is None:
            return ""
        return self.private_key.hex()

    class Config:
        populate_by_name = True
