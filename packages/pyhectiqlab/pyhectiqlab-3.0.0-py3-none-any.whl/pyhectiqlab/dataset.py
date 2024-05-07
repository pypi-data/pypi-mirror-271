import os
import clisync
from typing import Optional, List, Union
import asyncio

from pyhectiqlab.tag import Tag
from pyhectiqlab.project import Project
from pyhectiqlab.block import Block
from pyhectiqlab.block import Block
from pyhectiqlab.client import Client
from pyhectiqlab.decorators import functional_alias, online_method
from pyhectiqlab.utils.path import list_all_files_in_dir, extract_host_from_source
from pyhectiqlab.utils.itertools import batched


class Dataset:
    _client: Client = Client

    @staticmethod
    @online_method
    @functional_alias("create_dataset")
    @clisync.include()
    def create(
        name: str,
        source: str,
        host: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        block: Optional[str] = None,
        run_id: Optional[str] = None,
        project: Optional[str] = None,
        upload: Optional[bool] = False,
    ):
        """Create a dataset.

        Supported cloud storages:
        - Amazon S3
        - Google Cloud Storage

        Args:
            name (str): Name of the dataset.
            source (str): Path to the dataset. If your dataset is located in a local directory, the path should be the directory path (e.g., "/path/to/dataset"). If
                the dataset is located in a cloud storage, the path should be the URL of the dataset (e.g., "s3://bucket/dataset").
            host (str, optional): Source of the dataset. Default: None. If the dataset is located in a local directory,
                the resource could be your hostname or leave it empty. If the dataset is located in a cloud storage, the resource should be the cloud storage name ("s3" or "gs")
            version (str]): Version of the dataset. Default: None.
            description (str, optional): Description of the dataset. Default: None.
            block (str, optional): Block of the dataset. Default: None.
            project (str, optional): Project of the dataset. Default: None.
            run_id (str, optional): Run of the dataset. Default: None.
            upload (bool): If True, upload the dataset to the Lab. Default: False.
        """
        from pyhectiqlab.run import Run

        project = Project.get(project)
        run_id = Run.get_id(run_id)
        block = Block.get(block)
        if project is None:
            return

        if name is None:
            raise ValueError("The `name` parameter is required.")

        if source is None:
            raise ValueError("The `path` parameter is required.")
        source = os.path.abspath(source)
        host = extract_host_from_source(source)

        if block:
            if not "::" in block:
                block = Block.format_id(block, project)

        data = {
            "name": name,
            "description": description,
            "version": version,
            "host": host,
            "source": source,
            "block": block,
            "project": project,
            "root_run": run_id,
        }
        dataset = Dataset._client.post("/app/datasets", wait_response=True, json=data)
        if upload and host not in ["s3", "gs"]:
            Dataset.upload(id=dataset["id"], path=source)

        if run_id is not None:
            Dataset.attach(name=name, version=version, run_id=run_id, project=project)
        return dataset

    @staticmethod
    @online_method
    @functional_alias("upload_dataset")
    @clisync.include()
    def upload(id: str, path: str):
        """Upload local files to a dataset hosted in the Lab."""
        all_files = list_all_files_in_dir(path)
        batch_size = 50
        Dataset._id = dataset_id = id
        for batch in batched(all_files, batch_size):
            # Create many files
            batch_body = [{"name": os.path.relpath(f, start=path), "num_bytes": os.path.getsize(f)} for f in batch]
            files = Dataset._client.post(
                f"/app/datasets/{dataset_id}/files", wait_response=True, json={"files": batch_body}
            )["results"]

            # For each file in batch, get the policy in files (use name for finding the file)
            sorted_files = []
            for el in batch:
                file = [f.get("upload_policy") for f in files if f["name"] == os.path.relpath(el, start=path)][0]
                sorted_files.append(file)
            # Upload dataset files
            asyncio.run(Dataset._client.upload_many(paths=batch, policies=sorted_files))

    @staticmethod
    @online_method
    @functional_alias("retrieve_dataset")
    @clisync.include(wait_response=True)
    def retrieve(
        name: str,
        version: str,
        project: str,
        fields: Optional[List[str]] = None,
        wait_response: bool = True,  # This must be True, else no retrieve is possible.
    ):
        """Retrieve a dataset

        Args:
            name (str): Name of the dataset
            project (str): Project of the dataset
            version (str): Version of the dataset
            fields (list[str], optional): Fields to retrieve. Default: None.
        """
        body = Dataset._client.get(
            f"/app/datasets/retrieve",
            params={
                "name": name,
                "project": project,
                "version": version,
                "fields": fields or [],
            },
            wait_response=True,
        )
        return body

    @staticmethod
    @online_method
    @functional_alias("list_datasets")
    @clisync.include()
    def list(
        project: Optional[str] = None,
        search: Optional[str] = None,
        author: Optional[str] = None,
        block: Optional[str] = None,
        blocks: Optional[List[str]] = None,
        keep_latest_version: bool = False,
        fields: Optional[List[str]] = [],
        page: Optional[int] = 1,
        limit: Optional[int] = 100,
        order_by: Optional[str] = "created_at",
        order_direction: Optional[str] = "desc",
        wait_response: bool = False,
    ):
        """List the datasets

        Args:
            project (str, optional): Project of the dataset.
            block (str, optional): Block of the dataset.
            search (str, optional): Search string.
            author (str, optional): Author of the dataset.
            blocks (list[str], optional): Blocks of the dataset.
            keep_latest_version (bool, optional): If True, group by the latest version of dataset name and return only the latest version of each dataset name.
            fields (list[str], optional): Fields to retrieve.
            page (int, optional): Page number.
            limit (int, optional): Limit of the datasets.
            order_by (str, optional): Order by.
            order_direction (str, optional): Order direction.
            wait_response (bool): Wait for the response from the server. Default: False.
        """
        block = Block.get(block)
        if block is not None:
            if not "::" in block:
                block = Block.format_id(block, project)

        params = {
            "project": project,
            "block": block,
            "search": search,
            "author": author,
            "blocks": blocks,
            "keep_latest_version": keep_latest_version or True,
            "fields": fields,
            "page": page,
            "limit": limit,
            "order_by": order_by,
            "order_direction": order_direction,
        }

        return Dataset._client.get("/app/datasets", params=params, wait_response=wait_response)

    @staticmethod
    @online_method
    @functional_alias("update_dataset")
    @clisync.include()
    def update(
        id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        block: Optional[str] = None,
        wait_response: bool = False,
    ):
        """Update a dataset

        Args:
            id (str): ID of the dataset.
            name (str, optional): Name of the dataset.
            description (str, optional): Description of the dataset.
            version (str, optional): Version of the dataset.
            block (str, optional): Block of the dataset.
            wait_response (bool): Wait for the response from the server. Default: False
        """
        if not id:
            return
        return Dataset._client.put(
            f"/app/datasets/{id}",
            json={"name": name, "description": description, "version": version, "block": block},
            wait_response=wait_response,
        )

    @staticmethod
    @online_method
    @functional_alias("delete_dataset")
    @clisync.include()
    def delete(
        id: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        project: Optional[str] = None,
        wait_response: bool = False,
    ):
        """Delete a dataset.

        Args:
            id (str): ID of the dataset.
            name (str, optional): Name of the dataset.
            version (str, optional): Version of the dataset.
            project (str, optional): Project of the dataset.
            wait_response (bool): Wait for the response from the server. Default: False
        """
        assert id or (name and version and project), "Either `id` or `name`, `version` and `project` must be provided."
        if not id:
            dataset = Dataset.retrieve(name=name, project=project, version=version, fields=["id"])
            if not dataset:
                return
            id = dataset["id"]
        return Dataset._client.delete(f"/app/datasets/{id}", wait_response=wait_response)

    @staticmethod
    @online_method
    @functional_alias("download_dataset")
    @clisync.include()
    def download(
        name: str,
        version: str,
        project: Optional[str] = None,
        path: Optional[str] = "./",
        wait_response: bool = False,
    ):
        """Download a dataset

        Args:
            name (str): Name of the dataset.
            version (str): Version of the dataset.
            project (str, optional): Project of the dataset.
            path (str): Path to download the dataset. Default: "./".
            wait_response (bool): Wait for the response from the server. Default: False.
        """
        path = path or "./"
        path = os.path.join(path, f"{name}-{version.replace('.', '-')}")
        os.makedirs(path, exist_ok=True)
        Dataset.attach(name=name, version=version, project=project)

        async def composition():
            dataset = Dataset.retrieve(name=name, project=project, version=version, fields=["id"])
            if not dataset:
                return
            dataset_id = dataset["id"]

            num_results = 0
            total_results = 1
            page = 1
            while not num_results == total_results:
                files = Dataset._client.get(
                    f"/app/datasets/{dataset_id}/files/",
                    params={"page": page, "limit": 50, "fields": ["download_url", "name", "num_bytes"]},
                    wait_response=True,
                )
                total_results = files["total_results"]

                await Dataset._client.download_many(
                    urls=[file["download_url"] for file in files["results"]],
                    local_paths=[os.path.join(path, file["name"]) for file in files["results"]],
                    num_bytes=[file["num_bytes"] for file in files["results"]],
                )
                num_results += len(files["results"])
                page += 1

            Dataset._client.post(f"/app/datasets/{dataset_id}/on-download-completed", wait_response=False)

        return Dataset._client.execute(composition, wait_response=wait_response, is_async_method=True)

    @staticmethod
    @online_method
    def attach(
        name: str,
        version: str,
        run_id: str,
        project: Optional[str] = None,
        wait_response: bool = False,
    ):
        """Attach a dataset to a run

        Args:
            name (str): Name of the dataset.
            version (str): Version of the dataset.
            run_id (str): ID of the run.
            project (str, optional): Project of the dataset.
            wait_response (bool): Wait for the response from the server. Default: False.
        """
        dataset = Dataset.retrieve(name=name, project=project, version=version, fields=["id"])
        if dataset is None or run_id is None:
            return
        return Dataset._client.post(
            f"/app/datasets/{dataset['id']}/attach-to-run/{run_id}", wait_response=wait_response
        )

    @staticmethod
    @online_method
    def detach(
        name: str,
        version: str,
        run_id: str,
        project: Optional[str] = None,
        wait_response: bool = False,
    ):
        """Detach a dataset from a run

        Args:
            name (str): Name of the dataset.
            version (str): Version of the dataset.
            run_id (str): ID of the run.
            project (str, optional): Project of the dataset.
            wait_response (bool, optional): Wait for the response from the server. Default: False.
        """
        dataset = Dataset.retrieve(name=name, project=project, version=version, fields=["id"])
        if not dataset:
            return
        dataset_id = dataset["id"]
        return Dataset._client.post(
            f"/app/datasets/{dataset_id}/detach-from-run/{run_id}", wait_response=wait_response
        )

    @staticmethod
    @online_method
    def add_tags(
        tags: Union[str, List[str]],
        name: str,
        version: str,
        project: Optional[str] = None,
    ):
        """Add tags to a dataset

        Args:
            tags (Union[str, List[str]]): Tags to add.
            name (str): Name of the dataset.
            version (str): Version of the dataset.
            project (str, optional): Project name. Default: None.
        """
        project = Project.get(project)
        dataset = Dataset.retrieve(name=name, project=project, version=version, fields=["id"])
        if not dataset:
            return
        dataset_id = dataset["id"]
        return Tag.attach_to_dataset(tags=tags, dataset_id=dataset_id, project=project)

    @staticmethod
    @online_method
    def detach_tag(
        tag: str,
        name: str,
        version: str,
        project: Optional[str] = None,
    ):
        """Remove a tag from the run.
        For functional alias, use `detach_tag_from_run`.

        Args:
            title (str): The new title of the run.
            name (str): Name of the dataset.
            version (str): Version of the dataset.
            project (str, optional): Project name. Default: None.
        """
        project = Project.get(project)
        dataset = Dataset.retrieve(name=name, version=version, project=project, fields=["id"])
        if not dataset:
            return
        dataset_id = dataset["id"]
        Tag.detach_from_dataset(tag=tag, dataset_id=dataset_id, project=project)
