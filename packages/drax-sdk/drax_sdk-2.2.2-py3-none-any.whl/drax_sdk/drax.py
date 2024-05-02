from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional, List
import os

from drax_sdk.clients.drax_core_client import DraxCoreClient
from drax_sdk.model.dto import (
    PagedResult,
    HandshakeRequest,
    HandshakeResponse,
    InstalledNode,
    FindNodeByIdsRequest,
    StateRequest,
    ConfigurationRequest,
    StateResponse,
)
from drax_sdk.model.node import NodeType, Node, State
from drax_sdk.model.event import Event
from drax_sdk.model.project import Project
from drax_sdk.utils.codec import encode_state
from drax_sdk.utils.keystore import KeyStore


class DraxConfigParams(BaseModel):
    project_id: Optional[str] = None
    api_key: str
    api_secret: str
    drax_core_url: str
    automation_url: str
    broker_port: int
    broker_host: str
    broker_vhost: str
    data_miner_url: str

    @classmethod
    def load_from_env(cls):
        load_dotenv()
        return cls(
            project_id=os.getenv("DRAX_PROJECT_ID"),
            api_key=os.getenv("DRAX_PROJECT_API_KEY"),
            api_secret=os.getenv("DRAX_PROJECT__API_SECRET"),
            drax_core_url=os.getenv("DRAX_CORE_URL"),
            automation_url=os.getenv("DRAX_AUTOMATION_URL"),
            broker_port=int(os.getenv("DRAX_BROKER_PORT")),
            broker_host=os.getenv("DRAX_BROKER_HOST"),
            broker_vhost=os.getenv("DRAX_BROKER_VHOST"),
            data_miner_url=os.getenv("DRAX_DATA_MINER_URL"),
        )


class DraxCore:

    client: DraxCoreClient

    def __init__(self, client: DraxCoreClient):
        self.client = client

    def register_node_type(self, node_type: NodeType) -> NodeType:
        return self.client.register_node_type(node_type)

    def update_node_type(self, node_type: NodeType) -> None:
        return self.client.update_node_type(node_type)

    def get_node_type_by_id(self, node_type_id: str) -> NodeType:
        return self.client.get_node_type_by_id(node_type_id)

    def unregister_node_type(self, node_type_id: str) -> None:
        self.client.unregister_node_type(node_type_id)

    # todo: da controllare perche il client non sembra avere parametri
    def list_node_types(self) -> PagedResult[NodeType]:
        return self.client.list_node_types()

    def handshake(self, request: HandshakeRequest) -> HandshakeResponse:
        return self.client.handshake(request)

    def get_my_project(self) -> Project:
        return self.client.get_my_project()

    def get_project_by_id(self, id: str) -> Project:
        return self.client.get_project_by_id(id)

    def register_project(self, project: Project) -> Project:
        return self.client.register_project(project)

    def update_project(self, project: Project) -> None:
        self.client.update_project(project)

    def unregister_project(self, id: str) -> None:
        self.client.unregister_project(id)

    def install_node(self, node: Node) -> InstalledNode:
        return self.client.install_node(node)

    # def generate_key_pair(self, request: ECDHKeysPairRequest) -> ECDHKeysPairResponse:
    #     return self.client.generate_keys_pair(request)
    #
    # def revoke_key_pair(self, request: ECDHRevokeRequest) -> ECDHRevokeResponse:
    #     return self.client.revoke_key(request)

    def update_node(self, node: Node) -> None:
        self.client.update_node(node)

    def uninstall_node(self, node_id: str) -> None:
        self.client.uninstall_node(node_id)

    def get_node_by_id(self, node_id: str) -> Node:
        return self.client.get_node_by_id(node_id)

    def get_nodes_by_ids(
        self, find_node_by_ids_request: FindNodeByIdsRequest
    ) -> List[Node]:
        return self.client.get_nodes_by_ids(find_node_by_ids_request)

    def list_projects(self, page: int = None, size: int = None) -> PagedResult[Project]:
        return self.client.list_projects()

    def list_nodes(
        self, project_id: str, keyword: str, page: int, size: int
    ) -> PagedResult[Node]:
        return self.client.list_nodes(project_id, keyword, page, size)

    def list_states(
        self,
        node_id: str,
        project_id: str = None,
        from_time: int = None,
        to_time: int = None,
        fetch_size: int = None,
    ) -> PagedResult[StateResponse]:
        return self.client.list_states(
            node_id=node_id,
            project_id=project_id,
            from_time=from_time,
            to_time=to_time,
            fetch_size=fetch_size,
        )

    def list_nodes_states(
        self,
        project_id: str,
        find_node_by_ids_request: FindNodeByIdsRequest,
        start: int,
        end: int,
        page: int,
        size: int,
    ) -> PagedResult[StateResponse]:
        return self.client.list_nodes_states(
            project_id, find_node_by_ids_request, start, end, page, size
        )

    def set_state(self, node_id: str, state_request: StateRequest) -> None:
        self.client.set_state(node_id, state_request)

    def get_state(self, node_id: str) -> StateResponse:
        return self.client.get_state(node_id)

    def set_configuration(
        self, node_id: str, configuration: ConfigurationRequest
    ) -> None:
        self.client.set_configuration(node_id, configuration)

    def invoke(self, event: Event) -> None:
        self.client.invoke(event)


class Drax:
    def __init__(self, config: DraxConfigParams):
        self.config = config
        self.core = DraxCore(
            DraxCoreClient(config.drax_core_url, config.api_key, config.api_secret)
        )
        # self.drax_automation = DraxAutomation(
        #     AutomationClient(config.automation_url, config.api_key, config.api_secret)
        # )
        # self.drax_data_miner = DraxDataMiner(
        #     DataMinerClient(config.data_miner_url, config.api_key, config.api_secret)
        # )
        # self.drax_ai = DraxAi(
        #     AiClient(config.ai_url, config.api_key, config.api_secret)
        # )
        # self.broker = AmqpDraxBroker(config)

    def start(self):
        # self.broker.start()
        pass

    def stop(self):
        # self.broker.stop()
        pass

    # def get_backend(self):
    #     return self.drax_backend
    #
    # def get_automation(self):
    #     return self.drax_automation
    #
    # def get_data_miner(self):
    #     return self.drax_data_miner

    def set_state(
        self,
        state: State,
        node_id: str = None,
        cryptography_disabled=False,
        urn: str = None,
    ):
        # self.broker.set_state(state.node_id, None, state, cryptography_disabled)
        node_id = node_id if node_id else state.node_id
        if not node_id and not urn:
            raise ValueError("Either node_id or urn must be provided")

        node_private_key = KeyStore.get_private_key(node_id)

        request = StateRequest(
            node_id=state.node_id,
            state=encode_state(node_private_key, state),
            cryptography_disabled=cryptography_disabled,
            urn=urn,
        )
        self.core.set_state(node_id, request)

    def set_configuration(self, configuration, cryptography_disabled=False):
        # self.broker.set_configuration(
        #     configuration.node_id, None, configuration, cryptography_disabled
        # )
        pass

    # def add_configuration_listener(self, topic, listener):
    #     self.broker.add_configuration_listener(topic, listener)
    #
    # def add_state_listener(self, topic, listener):
    #     self.broker.add_state_listener(topic, listener)
