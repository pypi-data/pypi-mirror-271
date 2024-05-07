import dataclasses
import pathlib
import typing as t
import uuid

import mantik.utils.mantik_api.client as client


@dataclasses.dataclass
class PostPutDataRepository:
    uri: str
    data_repository_name: t.Optional[str] = None
    access_token: t.Optional[str] = None
    description: t.Optional[str] = None

    @classmethod
    def from_target(
        cls,
        target: t.Union[str, pathlib.Path],
        user: str,
        data_repository_name: t.Optional[str],
        data_repository_description: t.Optional[str],
    ):
        return cls(
            uri=str(target),
            data_repository_name=data_repository_name
            if data_repository_name
            else str(target),
            description=data_repository_description
            if data_repository_description
            else (
                f"This data repository with path: {str(target)} "
                f"was uploaded by {user}"
            ),
        )

    def to_dict(self) -> t.Dict:
        return {
            "dataRepositoryName": self.data_repository_name,
            "uri": self.uri,
            "accessToken": self.access_token,
            "description": self.description,
        }


def add(
    add_data_repository: PostPutDataRepository,
    project_id: uuid.UUID,
    token: str,
):
    data = add_data_repository.to_dict()
    endpoint = f"/projects/{str(project_id)}/data"
    response = client.send_request_to_mantik_api(
        method="POST", data=data, url_endpoint=endpoint, token=token
    )
    client.logger.info(
        f'A new data repository with ID: {response.json()["dataRepositoryId"]} '
        f"and name: {add_data_repository.data_repository_name} at "
        f"{add_data_repository.uri} has been created"
    )
    return response.json()["dataRepositoryId"]


def delete(
    project_id: uuid.UUID,
    data_repository_id: uuid.UUID,
    token: str,
) -> None:
    data = {}
    endpoint = f"/projects/{str(project_id)}/data/{str(data_repository_id)}"
    client.send_request_to_mantik_api(
        method="DELETE", data=data, url_endpoint=endpoint, token=token
    )
    client.logger.info(
        f"Data repository with ID: {data_repository_id} has been deleted"
    )


def get_all(
    project_id: uuid.UUID,
    token: str,
) -> t.List[t.Dict]:
    endpoint = f"/projects/{str(project_id)}/data"
    response = client.send_request_to_mantik_api(
        method="GET", data={}, url_endpoint=endpoint, token=token
    )
    return response.json()["dataRepositories"]
