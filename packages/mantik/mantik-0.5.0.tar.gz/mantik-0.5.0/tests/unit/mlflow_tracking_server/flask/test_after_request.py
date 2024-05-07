import pytest


@pytest.mark.parametrize(
    ("max_results", "added_experiments", "allowed_to_see", "expected"),
    [
        (
            "1",
            ["Default", "test_experiment_1", "test_experiment_2"],
            ["Default"],
            ["Default"],
        ),
        (
            "3",
            ["Default", "test_experiment_1", "test_experiment_2"],
            ["Default", "test_experiment_1", "test_experiment_2"],
            ["Default", "test_experiment_1", "test_experiment_2"],
        ),
        (
            "2",
            ["Default", "test_experiment_1", "test_experiment_2"],
            ["Default", "test_experiment_1", "test_experiment_2"],
            ["test_experiment_2", "test_experiment_1"],
        ),
    ],
)
def test_get_experiment(
    client,
    mock_api_permissions,
    add_experiments_to_mlflow,
    max_results,
    added_experiments,
    allowed_to_see,
    expected,
    get_experiment_ids,
):
    add_experiments_to_mlflow(added_experiments)
    experiment_ids = get_experiment_ids(allowed_to_see)
    with mock_api_permissions(
        [
            (
                "POST",
                "mlflow/permissions/experiments",
                {
                    "allowed": True,
                    "message": "Allow for creating experiments and to search",
                    "experimentIds": experiment_ids,
                },
            )
        ]
    ):
        response = client.post(
            "api/2.0/mlflow/experiments/search",
            json={
                "max_results": max_results,
            },
            headers={"Authorization": "test-valid-token"},
        )
        assert response.status_code == 200
        assert sorted(
            [experiment["name"] for experiment in response.json["experiments"]]
        ) == sorted(expected)
        assert response.status_code == 200
