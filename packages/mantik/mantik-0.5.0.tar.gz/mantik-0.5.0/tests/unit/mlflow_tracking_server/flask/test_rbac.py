import uuid

import pytest


@pytest.mark.parametrize(
    ("response", "expected", "status"),
    [
        (
            {
                "allowed": True,
                "message": "This is a mock test",
                "experimentIds": None,
            },
            '"experiment_id": "0"',
            200,
        ),
        (
            {
                "allowed": False,
                "message": "This is a mock test",
                "experimentIds": None,
            },
            "Permission denied: This is a mock test",
            403,
        ),
    ],
)
def test_supported_endpoint(
    client, mock_api_permissions, response, expected, status
):
    with mock_api_permissions(
        [("POST", "mlflow/permissions/experiments", response)]
    ):
        response = client.get(
            "api/2.0/mlflow/experiments/get",
            json={
                "experiment_id": "0",
            },
            headers={"Authorization": "test-valid-token"},
        )
        assert expected in response.text
        assert response.status_code == status


def test_not_yet_supported_endpoint(client):
    response = client.get(
        "api/2.0/mlflow/runs/get",
        json={
            "run_id": "0",
        },
        headers={"Authorization": "test-valid-token"},
    )
    assert response.json["error_code"] == "RESOURCE_DOES_NOT_EXIST"
    assert response.status_code == 404


def test_request_from_api(client, api_base_url, set_unset_api_base_url):
    with set_unset_api_base_url:
        response = client.post(
            "api/2.0/mlflow/experiments/create",
            json={
                "name": uuid.uuid4().hex,
            },
            headers={
                "Authorization": "test-valid-token",
                "MantikOrigin": "MantikApi",
            },
        )
        assert response.status_code == 200, response.text
