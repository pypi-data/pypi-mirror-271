import logging
import os
import pathlib
import tempfile
import typing as t
import uuid

import mantik.runs.schemas as schemas
import mantik.utils.mantik_api as mantik_api
import mantik.utils.mantik_api.code_repository as code_api
import mantik.utils.mantik_api.experiment_repository as experiment_api


logger = logging.getLogger(__name__)


class LocalRunManager:
    def __init__(self):
        pass

    @classmethod
    def clone_git_repo(
        cls, uri: str, branch: str, target_directory: str
    ) -> None:
        try:
            import git
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "Please install git module: required to execute local runs"
            ) from e

        logger.debug(f"Cloning repo {uri}...")

        git.Repo.clone_from(uri, target_directory, branch=branch)

        logger.debug("Repo cloned.")

    @staticmethod
    def start_local_run(
        mlflow_experiment_id: str,
        data: schemas.RunConfiguration,
        project_id: uuid.UUID,
        mantik_token: str,
        uri: str,
    ) -> None:
        # Lazy import so that mantik can be used without mlflow
        import mlflow
        import mantik.mlflow
        import mantik.utils.mlflow

        logger.info(f"Starting mlflow run: '{data.name}' ...")
        mlflow.set_tracking_uri(
            os.getenv(
                mantik.utils.mlflow.TRACKING_URI_ENV_VAR,
                mantik.utils.mlflow.DEFAULT_TRACKING_URI,
            )
        )
        with mantik.mlflow.start_run(
            experiment_id=mlflow_experiment_id,
            run_name=data.name,
        ) as active_run:
            data.mlflow_run_id = active_run.info.run_id
            run_id = save_run_data(
                data=data, project_id=project_id, mantik_token=mantik_token
            )
            mantik_api.run.update_run_status(
                project_id=project_id,
                token=mantik_token,
                status=active_run.info.status,
                run_id=run_id,
            )
        try:
            _run = mlflow.run(
                uri=uri,
                backend="local",
                experiment_id=mlflow_experiment_id,
                run_name=data.name,
                entry_point=data.entry_point,
                parameters=data.mlflow_parameters,
                backend_config={
                    mantik.mlflow.get_local_backend_config_run_id_env_var(): active_run.info.run_id  # noqa: E501
                },
                build_image=True,
                docker_args={
                    "e": f"{mantik.utils.mlflow.TRACKING_TOKEN_ENV_VAR}={os.environ[mantik.utils.mlflow.TRACKING_TOKEN_ENV_VAR]}"  # noqa: E501
                },
            )
        except KeyboardInterrupt as e:
            logger.warning(
                "Keyboard interrupt, setting Mantik run status to KILLED"
            )
            mantik_api.run.update_run_status(
                project_id=project_id,
                token=mantik_token,
                status="KILLED",
                run_id=run_id,
            )
            raise e
        # MlflowException is raised when something goes wrong with mlflow
        # FileNotFoundError is raised when pyenv or conda are not found
        except (mlflow.exceptions.MlflowException, FileNotFoundError) as e:
            logger.warning(
                "Failed to execute run, setting Mantik run status to FAILED"
            )
            mantik_api.run.update_run_status(
                project_id=project_id,
                token=mantik_token,
                status="FAILED",
                run_id=run_id,
            )
            raise e
        logger.debug("Run finished successfully")
        mantik_api.run.update_run_status(
            project_id=project_id,
            token=mantik_token,
            status=_run.get_status(),
            run_id=run_id,
        )


def fetch_code_and_experiment(
    project_id: uuid.UUID,
    code_repository_id: uuid.UUID,
    experiment_repository_id: uuid.UUID,
    mantik_token: str,
) -> t.Tuple[code_api.CodeRepository, experiment_api.ExperimentRepository]:
    logger.debug("Fetching code and experiment from Mantik API...")
    code = code_api.get_one(
        code_repository_id=code_repository_id,
        project_id=project_id,
        token=mantik_token,
    )
    experiment = experiment_api.get_one(
        experiment_repository_id=experiment_repository_id,
        project_id=project_id,
        token=mantik_token,
    )
    logger.debug(f"Fetched {code} and {experiment}")
    return code, experiment


def save_run_data(
    data: schemas.RunConfiguration, project_id: uuid.UUID, mantik_token: str
) -> uuid.UUID:
    logger.debug(f"Saving data... {data}")

    response = mantik_api.run.save_run(
        project_id=project_id,
        run_data=data.to_post_payload(),
        token=mantik_token,
    )

    logger.debug("Results saved to Mantik API")
    return uuid.UUID(response.json()["runId"])


def run(
    data: schemas.RunConfiguration,
    project_id: uuid.UUID,
    mantik_token: str,
    run_manager: LocalRunManager = LocalRunManager(),
):
    code, experiment = fetch_code_and_experiment(
        project_id=project_id,
        code_repository_id=data.code_repository_id,
        experiment_repository_id=data.experiment_repository_id,
        mantik_token=mantik_token,
    )

    data.name = experiment_api.get_unique_run_name(
        experiment_repository_id=data.experiment_repository_id,
        project_id=project_id,
        token=mantik_token,
        run_name=data.name,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        run_manager.clone_git_repo(
            uri=code.uri,
            branch=data.commit or data.branch,
            target_directory=temp_dir,
        )

        run_manager.start_local_run(
            uri=path_directory_of_mlproject_file(
                str(
                    pathlib.Path(temp_dir).joinpath(
                        data.mlflow_mlproject_file_path
                    )
                )
            ),
            data=data,
            mlflow_experiment_id=experiment.mlflow_experiment_id,
            mantik_token=mantik_token,
            project_id=project_id,
        )


def path_directory_of_mlproject_file(mlproject_file_path: str) -> str:
    return str(pathlib.Path(mlproject_file_path).parent)
