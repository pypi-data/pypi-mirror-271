import pytest

from pyhectiqlab import Run
from util import mock_client


@pytest.fixture
def config():
    return {"param": "test", "x": 1}


def test_run_create():
    with mock_client(Run) as r:
        run = r(title="test run", project="hectiq-ai/test")


def test_run_retrieve():
    run = Run(rank=1, project="hectiq-ai/test")


@pytest.mark.filterwarnings("error")
def test_run_retrieve_by_id():

    # retrieving first run by id
    run_id = "7abdd377-b702-452c-bfe5-df13f34a99d9"
    run = Run.retrieve_by_id(run_id=run_id)
    assert run is not None
    assert run["id"] == run_id


@pytest.mark.filterwarnings("error")
def test_run_retrieve_not_existing_rank_raises_warning():
    invalid_rank = 1000
    with pytest.raises(UserWarning):
        run = Run(rank=invalid_rank, project="hectiq-ai/test")


def test_run_exists():
    assert Run.exists(rank=1, project="hectiq-ai/test") == True
    assert Run.exists(rank=1000, project="hectiq-ai/test") == False


def test_run_add_config(config):
    run = Run(rank=1, project="hectiq-ai/test")
    config = {"param": "test", "x": 1}
    run.add_config(config)


def test_run_retrieve_config(config):
    run = Run(rank=1, project="hectiq-ai/test")
    assert run.retrieve_config() == config


def test_run_add_artifact():
    import os

    with mock_client(Run) as r:
        run = r(rank=1, project="hectiq-ai/test")
        path = os.path.join(os.path.dirname(__file__), "dummy/artifact.txt")
        res = run.add_artifact(path, name="content.txt", wait_response=True)


def test_run_set_status():
    run = Run(rank=1, project="hectiq-ai/test")
    run.set_status("test status")


def test_run_add_tag():
    run = Run(rank=1, project="hectiq-ai/test")
    run.add_tags("some")


def test_run_detach_tag():
    run = Run(rank=1, project="hectiq-ai/test")
    run.add_tags("some")
    run.detach_tag("some")


if __name__ == "__main__":
    pass
