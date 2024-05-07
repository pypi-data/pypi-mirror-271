import pytest
import os
from util import mock_client


@pytest.fixture
def dummy():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "dummy/"))


@pytest.fixture
def data_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))


@pytest.fixture
def clear_data(data_path):
    yield
    import shutil

    shutil.rmtree(data_path, ignore_errors=True)


def test_model_create(dummy):
    import os
    from pyhectiqlab import Model

    with mock_client(Model) as m:
        m.create(name="test-model", project="hectiq-ai/test", path=dummy, wait_response=True)


def test_model_retrieve():
    from pyhectiqlab import Model

    model = Model.retrieve(name="test-model", version="1.0", project="hectiq-ai/test")
    assert model["name"] == "test-model"
    assert model["version"] == "1.0"


def test_model_download(data_path, clear_data):
    from pyhectiqlab import Model

    Model.download(name="test-model", version="1.4", project="hectiq-ai/test", path=data_path, wait_response=True)


def test_model_add_tag():
    from pyhectiqlab import Model

    Model.add_tags(tags=["test", "model"], name="test-model", version="1.0", project="hectiq-ai/test")


if __name__ == "__main__":
    pass
