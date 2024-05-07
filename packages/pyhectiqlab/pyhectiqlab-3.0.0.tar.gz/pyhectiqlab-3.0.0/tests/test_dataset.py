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


# def test_dataset_create_and_upload(dummy):
#     import os
#     from pyhectiqlab import Dataset
#     from pyhectiqlab.client import Client

#     with mock_client(Dataset) as d:
#         d.create(name="test-dataset", project="hectiq-ai/test", source=dummy, upload=True)


def test_dataset_retrieve():
    from pyhectiqlab import Dataset

    dataset = Dataset.retrieve(name="test-dataset", version="1.3", project="hectiq-ai/test")
    assert dataset["name"] == "test-dataset"
    assert dataset["version"] == "1.3"


def test_dataset_download(data_path, clear_data):
    from pyhectiqlab import Dataset

    Dataset.download(name="test-dataset", version="1.3", project="hectiq-ai/test", path=data_path, wait_response=True)


def test_dataset_add_tag():
    from pyhectiqlab import Dataset

    Dataset.add_tags(tags=["test", "dataset"], name="test-dataset", version="1.3", project="hectiq-ai/test")


if __name__ == "__main__":
    pass
