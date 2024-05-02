from typing import List

import requests

from drax_sdk.model.dto import (
    HandshakeRequest,
    StateRequest,
    ConfigurationRequest,
    FindNodeByIdsRequest,
    HandshakeResponse,
    PagedResult,
    InstalledNode,
    StateResponse,
)
from drax_sdk.model.event import Event
from drax_sdk.model.node import Node, NodeType, State
from drax_sdk.model.project import Project
from drax_sdk.utils.bytes_codec import bytes_to_base64, base64_to_bytes


class DraxCoreClient:
    service_url = ""
    api_key = ""
    api_secret = ""

    def __init__(self, service_url: str, api_key: str, api_secret: str):
        self.service_url = service_url
        self.api_key = api_key
        self.api_secret = api_secret

    def _get_headers(self):
        return {"drax-api-key": self.api_key, "drax-api-secret": self.api_secret}

    def handshake(self, request: HandshakeRequest) -> HandshakeResponse:
        payload = request.model_dump(by_alias=True)
        response = requests.post(
            self.service_url + "/handshake",
            data=payload,
            headers=self._get_headers(),
        )
        response.raise_for_status()

        return HandshakeResponse.model_validate(response.json())

    def register_node_type(self, node_type: NodeType) -> NodeType:
        response = requests.post(
            self.service_url + "/nodeTypes",
            headers=self._get_headers(),
            json=node_type.model_dump(by_alias=True),
        )
        response.raise_for_status()

        return NodeType.model_validate(response.json())

    def update_node_type(self, node_type: NodeType):
        response = requests.post(
            self.service_url + f"/nodeTypes/{node_type.id}",
            headers=self._get_headers(),
            json=node_type.model_dump(by_alias=True),
        )
        response.raise_for_status()

    def get_node_type_by_id(self, node_type_id: str) -> NodeType:
        response = requests.get(
            self.service_url + f"/nodeTypes/{node_type_id}", headers=self._get_headers()
        )
        response.raise_for_status()

        return NodeType.model_validate(response.json())

    def unregister_node_type(self, node_type_id: str):
        response = requests.delete(
            self.service_url + f"/nodeTypes/{node_type_id}", headers=self._get_headers()
        )
        response.raise_for_status()

    def list_node_types(self, paging_state: str) -> PagedResult[NodeType]:
        response = requests.get(
            self.service_url + "/nodeTypes",
            headers=self._get_headers(),
            params={"pagingState": paging_state},
        )
        response.raise_for_status()

        return PagedResult[NodeType].model_validate(response.json())

    def list_projects(self, paging_state: str = None) -> PagedResult[Project]:
        response = requests.get(
            self.service_url + "/projects",
            headers=self._get_headers(),
            params={"pagingState": paging_state},
        )
        response.raise_for_status()

        return PagedResult[Project].model_validate(response.json())

    def register_project(self, project: Project) -> Project:
        response = requests.post(
            self.service_url + "/projects",
            headers=self._get_headers(),
            json=project.model_dump(by_alias=True),
        )
        response.raise_for_status()

        return Project.model_validate(response.json())

    def update_project(self, project: Project):
        response = requests.post(
            self.service_url + f'/projects/{project["id"]}',
            headers=self._get_headers(),
            json=project.model_dump(by_alias=True),
        )
        response.raise_for_status()

    def get_project_by_id(self, project_id: str) -> Project:
        response = requests.get(
            self.service_url + f"/projects/{project_id}", headers=self._get_headers()
        )
        response.raise_for_status()

        return Project.model_validate(response.json())

    def unregister_project(self, project_id: str):
        response = requests.delete(
            self.service_url + f"/projects/{project_id}", headers=self._get_headers()
        )
        response.raise_for_status()

    def get_my_project(self) -> Project:
        response = requests.get(
            self.service_url + "/projects/my", headers=self._get_headers()
        )
        response.raise_for_status()

        return Project.model_validate(response.json())

    def get_next_project_id(self, project_id: str) -> str:
        response = requests.get(
            self.service_url + f"/projectsIds/next/{project_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.text

    def install_node(self, node: Node) -> InstalledNode:
        response = requests.post(
            self.service_url + "/nodes",
            headers=self._get_headers(),
            json=node.model_dump(by_alias=True),
        )
        response.raise_for_status()

        return InstalledNode.model_validate(base64_to_bytes(response.json()))

    def update_node(self, node: Node):
        json_data = bytes_to_base64(node.model_dump(by_alias=True))
        print(json_data)

        response = requests.post(
            self.service_url + f"/nodes/{node.id}",
            headers=self._get_headers(),
            json=json_data,
        )

        response.raise_for_status()

    def uninstall_node(self, node_id: str):
        response = requests.delete(
            self.service_url + f"/nodes/{node_id}", headers=self._get_headers()
        )
        response.raise_for_status()

    def get_node_by_id(self, node_id: str) -> Node:
        response = requests.get(
            self.service_url + f"/nodes/{node_id}", headers=self._get_headers()
        )
        response.raise_for_status()

        return Node.model_validate(base64_to_bytes(response.json()))

    def list_nodes(
        self, project_id: str, keyword=None, paging_state=None
    ) -> PagedResult[Node]:
        params = {"projectId": project_id}
        if keyword:
            params["keyword"] = keyword
        if paging_state:
            params["pagingState"] = paging_state
        response = requests.get(
            self.service_url + "/nodes", params=params, headers=self._get_headers()
        )
        response.raise_for_status()

        return PagedResult[Node].model_validate(base64_to_bytes(response.json()))

    def get_state(self, node_id: str) -> StateResponse:
        url = self.service_url + f"/nodes/{node_id}/state"
        response = requests.get(url, headers=self._get_headers())

        response.raise_for_status()

        return StateResponse.model_validate(response.json())

    def list_states(
        self,
        node_id: str,
        project_id: str = None,
        from_time: int = None,
        to_time: int = None,
        fetch_size: int = None,
    ) -> PagedResult[StateResponse]:
        params = {
            "projectId": project_id,
            "from": from_time,
            "to": to_time,
            "fetchSize": fetch_size,
        }
        response = requests.get(
            self.service_url + f"/nodes/{node_id}/states",
            params=params,
            headers=self._get_headers(),
        )
        response.raise_for_status()

        return PagedResult[StateResponse].model_validate(response.json())

    def list_nodes_states(
        self,
        project_id: str,
        find_node_by_ids_request: FindNodeByIdsRequest,
        from_time: int,
        to_time: int,
        fetch_size: int,
        paging_state: int,
    ) -> PagedResult[StateResponse]:
        params = {
            "projectId": project_id,
            "from": from_time,
            "to": to_time,
            "fetchSize": fetch_size,
            "pagingState": paging_state,
        }
        response = requests.post(
            self.service_url + "/states/find-by-node-ids",
            params=params,
            headers=self._get_headers(),
            json=find_node_by_ids_request.model_dump(by_alias=True),
        )
        response.raise_for_status()

        return PagedResult[StateResponse].model_validate(response.json())

    def set_state(self, node_id, request: StateRequest):
        json_data = bytes_to_base64(request.model_dump(by_alias=True))
        response = requests.post(
            self.service_url + f"/nodes/{node_id}/states",
            headers=self._get_headers(),
            json=json_data,
        )
        response.raise_for_status()

    def set_configuration(self, node_id, request: ConfigurationRequest):
        response = requests.post(
            self.service_url + f"/nodes/{node_id}/configurations",
            headers=self._get_headers(),
            json=request.model_dump(by_alias=True),
        )
        response.raise_for_status()

    def request_state_update(self, node_id: str):
        response = requests.post(
            self.service_url + f"/nodes/{node_id}/states/update",
            headers=self._get_headers(),
        )
        response.raise_for_status()

    def invoke(self, event: Event):
        response = requests.post(
            self.service_url + "/events/invoke",
            headers=self._get_headers(),
            json=event.model_dump(by_alias=True),
        )
        response.raise_for_status()

    def get_nodes_by_ids(self, request: FindNodeByIdsRequest) -> List[Node]:
        response = requests.post(
            self.service_url + "/nodes/find-by-ids",
            headers=self._get_headers(),
            json=request.model_dump(by_alias=True),
        )
        response.raise_for_status()

        return [Node.model_validate(node) for node in response.json()]
