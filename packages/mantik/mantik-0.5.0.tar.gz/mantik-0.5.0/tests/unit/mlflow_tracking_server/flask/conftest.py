import contextlib
import typing as t

import flask
import pytest
import requests_mock

import mantik.testing as testing
import mantik.utils.env as env
import mantik.utils.mantik_api.client as mantik_api_client
import mlflow_tracking_server.flask.app as flask_app
import tokens.verifier as verifier


@pytest.fixture()
def app(monkeypatch) -> flask.Flask:
    monkeypatch.setattr(
        verifier,
        "TokenVerifier",
        testing.mlflow_server.FakeTokenVerifier,
    )

    _app = flask_app.app
    _app.config.update(
        {
            "TESTING": True,
        }
    )

    yield _app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def api_path() -> str:
    return "/api/2.0/mlflow"


@pytest.fixture()
def api_base_url() -> str:
    return "https://api.dev.cloud.mantik.ai/"


@pytest.fixture()
@contextlib.contextmanager
def set_unset_api_base_url(api_base_url):
    env.set_env_vars({mantik_api_client._MANTIK_API_URL_ENV_VAR: api_base_url})
    yield
    env.unset_env_vars([mantik_api_client._MANTIK_API_URL_ENV_VAR])


@pytest.fixture()
def mock_api_permissions(set_unset_api_base_url, api_base_url):
    class Mocker:
        def __init__(self, mocked_urls: t.List[t.Tuple[str, str, t.Dict]]):
            """
            mocked_urls should be a list of tuples that contain:
            method: str e.g. GET, POST ...
            url: str e.g. mlflow/permissions/experiments"
            json: dict e.g. {
                    "allowed": True,
                    "message": "This is a mock test",
                    "experimentIds": None,
                }
            """
            self.mocker = requests_mock.Mocker(real_http=True)
            for method, url, json in mocked_urls:
                self.mocker.register_uri(
                    method,
                    api_base_url + url,
                    json=json,
                )

        def __enter__(self):
            env.set_env_vars(
                {mantik_api_client._MANTIK_API_URL_ENV_VAR: api_base_url}
            )
            return self.mocker.__enter__()

        def __exit__(self, type, value, traceback):
            env.unset_env_vars([mantik_api_client._MANTIK_API_URL_ENV_VAR])
            self.mocker.__exit__(type, value, traceback)

    return Mocker


@pytest.fixture()
def add_experiments_to_mlflow(client, mock_api_permissions):
    """
    Return the experiment ids of the added experiments
    """

    def wrapper(experiment_names: t.List[str]):
        with mock_api_permissions(
            [
                (
                    "POST",
                    "mlflow/permissions/experiments",
                    {
                        "allowed": True,
                        "message": "Allow for anything",
                        "experimentIds": None,
                    },
                )
            ]
        ):
            for name in experiment_names:
                response = client.post(
                    "api/2.0/mlflow/experiments/create",
                    json={"name": name},
                    headers={"Authorization": "test-valid-token"},
                )

                assert (
                    response.status_code == 200
                    or response.json["error_code"] == "RESOURCE_ALREADY_EXISTS"
                )

    return wrapper


@pytest.fixture()
def get_experiment_ids(client, mock_api_permissions):
    def wrapper(experiment_names: t.List[str]):
        with mock_api_permissions(
            [
                (
                    "POST",
                    "mlflow/permissions/experiments",
                    {
                        "allowed": True,
                        "message": "Allow for anything",
                        "experimentIds": None,
                    },
                )
            ]
        ):
            return [
                client.get(
                    "api/2.0/mlflow/experiments/get-by-name",
                    json={"experiment_name": name},
                    headers={"Authorization": "test-valid-token"},
                ).json["experiment"]["experiment_id"]
                for name in experiment_names
            ]

    return wrapper
