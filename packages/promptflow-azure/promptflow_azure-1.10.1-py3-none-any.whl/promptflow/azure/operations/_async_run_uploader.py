import asyncio
import json
import shutil
import tempfile
from pathlib import Path
from typing import Dict, List

from azure.core.exceptions import HttpResponseError, ResourceExistsError
from azure.storage.blob.aio import BlobServiceClient

from promptflow._cli._utils import get_instance_results, merge_jsonl_files
from promptflow._constants import PROMPTY_EXTENSION, OutputsFolderName
from promptflow._sdk._constants import (
    DEFAULT_ENCODING,
    CloudDatastore,
    FlowRunProperties,
    Local2Cloud,
    LocalStorageFilenames,
)
from promptflow._sdk._errors import RunNotFoundError, UploadInternalError, UploadUserError, UserAuthenticationError
from promptflow._sdk.entities import Run
from promptflow._utils.flow_utils import resolve_flow_path
from promptflow._utils.logger_utils import get_cli_sdk_logger
from promptflow.azure._storage.blob.client import _get_datastore_credential
from promptflow.exceptions import UserErrorException

logger = get_cli_sdk_logger()


class AsyncRunUploader:
    """Upload local run record to cloud"""

    IGNORED_PATTERN = ["__pycache__"]

    def __init__(self, run: Run, run_ops: "RunOperations", overwrite=True):
        self.run = run
        self.run_output_path = Path(run.properties[FlowRunProperties.OUTPUT_PATH])
        self.run_ops = run_ops
        self.overwrite = overwrite
        self.datastore = self._get_datastore_with_secrets()
        self.blob_service_client = self._init_blob_service_client()

    def _get_datastore_with_secrets(self):
        logger.debug("Getting datastores with secrets.")
        operations = self.run_ops._datastore_operations
        default_datastore = operations.get_default(include_secrets=True)
        artifact_datastore = operations.get(name=CloudDatastore.ARTIFACT, include_secrets=True)
        return {
            CloudDatastore.DEFAULT: default_datastore,
            CloudDatastore.ARTIFACT: artifact_datastore,
        }

    def _init_blob_service_client(self):
        result = {}
        for name, datastore in self.datastore.items():
            logger.debug(f"Initializing blob service client for datastore {name!r}.")
            account_url = f"{datastore.account_name}.blob.{datastore.endpoint}"
            # use credential from datastore, in this way user does not need RBAC role "Storage Blob Data Contributor"
            # to perform write operation on the blob storage.
            credential = _get_datastore_credential(datastore, self.run_ops._datastore_operations)
            if not credential:
                raise UploadInternalError(f"Failed to get a valid credential from datastore {name!r}.")
            result[name] = BlobServiceClient(account_url=account_url, credential=credential)
        return result

    def _check_run_exists(self):
        """Check if run exists in cloud."""
        try:
            self.run_ops.get(self.run.name)
        except RunNotFoundError:
            # go ahead to upload if run does not exist
            pass
        else:
            msg_prefix = f"Run record {self.run.name!r} already exists in cloud"
            if self.overwrite is True:
                logger.warning(f"{msg_prefix}. Overwrite is set to True, will overwrite existing run record.")
            else:
                raise UploadUserError(f"{msg_prefix}. Overwrite is set to False, cannot upload the run record.")

    async def upload(self) -> Dict:
        """Upload run record to cloud."""
        # check if run already exists in cloud
        self._check_run_exists()

        # upload run details to cloud
        error_msg_prefix = f"Failed to upload run {self.run.name!r}"
        try:
            async with self.blob_service_client[CloudDatastore.DEFAULT], self.blob_service_client[
                CloudDatastore.ARTIFACT
            ]:
                # upload other artifacts
                tasks = [
                    # put async functions in tasks to run in coroutines
                    self._upload_flow_artifacts(),
                    self._upload_node_artifacts(),
                    self._upload_run_outputs(),
                    self._upload_logs(),  # overall logs
                    self._upload_snapshot(),
                    self._upload_flow_logs(),  # detailed logs for each line run
                    self._upload_instance_results(),
                ]
                results = await asyncio.gather(*tasks)

                # merge the results to be a dict
                result_dict = {
                    OutputsFolderName.FLOW_ARTIFACTS: results[0],
                    OutputsFolderName.NODE_ARTIFACTS: results[1],
                    OutputsFolderName.FLOW_OUTPUTS: results[2],
                    LocalStorageFilenames.LOG: results[3],
                    LocalStorageFilenames.SNAPSHOT_FOLDER: results[4],
                    LocalStorageFilenames.FLOW_LOGS_FOLDER: results[5],
                    Local2Cloud.FLOW_INSTANCE_RESULTS_FILE_NAME: results[6],
                }
                return result_dict

        except UserAuthenticationError:
            raise
        except UploadUserError:
            raise
        except Exception as e:
            raise UploadInternalError(f"{error_msg_prefix}. Error: {e}") from e

    async def _upload_flow_artifacts(self) -> str:
        """Upload run artifacts to cloud. Return the cloud relative path of flow artifacts folder."""
        logger.debug(f"Uploading flow artifacts for run {self.run.name!r}.")
        # need to merge jsonl files before uploading
        with tempfile.TemporaryDirectory() as temp_dir:
            local_folder = self.run_output_path / f"{OutputsFolderName.FLOW_ARTIFACTS}"
            temp_local_folder = Path(temp_dir) / f"{OutputsFolderName.FLOW_ARTIFACTS}"
            logger.debug("Merging run artifacts jsonl files.")
            merge_jsonl_files(local_folder, temp_local_folder)
            remote_folder = f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_ARTIFACTS}/{self.run.name}"
            # upload the artifacts folder to blob
            await self._upload_local_folder_to_blob(temp_local_folder, remote_folder)
            # upload updated meta.json to cloud
            await self._upload_meta_json(temp_local_folder)
            return f"{remote_folder}/{OutputsFolderName.FLOW_ARTIFACTS}"

    async def _upload_meta_json(self, temp_dir: Path):
        """
        Upload meta.json to cloud, the content should be updated to align with cloud run meta.json.
        Return the cloud relative path of meta.json file.
        """
        content = {"batch_size": 25}
        local_temp_file = temp_dir / LocalStorageFilenames.META
        with open(local_temp_file, "w", encoding=DEFAULT_ENCODING) as f:
            json.dump(content, f)
        remote_file = (
            f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_ARTIFACTS}/"
            f"{self.run.name}/{LocalStorageFilenames.META}"
        )
        await self._upload_local_file_to_blob(local_temp_file, remote_file)
        return remote_file

    async def _upload_node_artifacts(self) -> str:
        """Upload node artifacts to cloud. Return the cloud relative path of node artifacts folder."""
        logger.debug(f"Uploading node artifacts for run {self.run.name!r}.")
        local_folder = self.run_output_path / f"{OutputsFolderName.NODE_ARTIFACTS}"
        remote_folder = f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_ARTIFACTS}/{self.run.name}"
        await self._upload_local_folder_to_blob(local_folder, remote_folder)
        return f"{remote_folder}/{OutputsFolderName.NODE_ARTIFACTS}"

    async def _upload_run_outputs(self) -> str:
        """Upload run outputs to cloud. Return the cloud relative path of run outputs folder."""
        logger.debug(f"Uploading run outputs for run {self.run.name!r}.")
        local_folder = self.run_output_path / f"{OutputsFolderName.FLOW_OUTPUTS}"
        remote_folder = f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_ARTIFACTS}/{self.run.name}"
        await self._upload_local_folder_to_blob(local_folder, remote_folder)
        return f"{remote_folder}/{OutputsFolderName.FLOW_OUTPUTS}"

    async def _upload_logs(self) -> str:
        """Upload overall logs to cloud. Return the cloud relative path of logs file"""
        logger.debug(f"Uploading logs for run {self.run.name!r}.")
        local_file = self.run_output_path / LocalStorageFilenames.LOG
        remote_file = f"{Local2Cloud.BLOB_EXPERIMENT_RUN}/dcid.{self.run.name}/{Local2Cloud.EXECUTION_LOG}"
        await self._upload_local_file_to_blob(local_file, remote_file, target_datastore=CloudDatastore.ARTIFACT)
        return remote_file

    async def _upload_snapshot(self) -> str:
        """Upload run snapshot to cloud. Return the cloud relative path of flow definition file."""
        logger.debug(f"Uploading snapshot for run {self.run.name!r}.")
        local_folder = self.run_output_path / LocalStorageFilenames.SNAPSHOT_FOLDER

        # parse the flow definition file
        run_flow_path = Path(self.run.properties[FlowRunProperties.FLOW_PATH]).name
        if str(run_flow_path).endswith(PROMPTY_EXTENSION):
            # for prompty flow run, get prompty file name from properties/flow_path
            flow_file = run_flow_path
        else:
            # for some types of flex flow, even there is no flow.flex.yaml in the original flow folder,
            # it will be generated in the snapshot folder in the .runs folder, so we can upload it to cloud as well.
            _, flow_file = resolve_flow_path(local_folder)

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_local_folder = Path(temp_dir) / self.run.name
            shutil.copytree(local_folder, temp_local_folder)
            remote_folder = f"{Local2Cloud.BLOB_ROOT_RUNS}"
            await self._upload_local_folder_to_blob(temp_local_folder, remote_folder)
            return f"{remote_folder}/{self.run.name}/{flow_file}"

    async def _upload_metrics(self) -> None:
        """Upload run metrics to cloud."""
        logger.debug(f"Uploading metrics for run {self.run.name!r}.")
        local_folder = self.run_output_path / LocalStorageFilenames.METRICS
        remote_folder = f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_METRICS}/{self.run.name}"
        await self._upload_local_folder_to_blob(local_folder, remote_folder)

    async def _upload_flow_logs(self) -> str:
        """Upload flow logs for each line run to cloud."""
        logger.debug(f"Uploading flow logs for run {self.run.name!r}.")
        local_folder = self.run_output_path / LocalStorageFilenames.FLOW_LOGS_FOLDER
        remote_folder = f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_ARTIFACTS}/{self.run.name}"
        await self._upload_local_folder_to_blob(local_folder, remote_folder)
        return f"{remote_folder}/{LocalStorageFilenames.FLOW_LOGS_FOLDER}"

    async def _upload_instance_results(self) -> str:
        """Upload instance results to cloud."""
        logger.debug(f"Uploading instance results for run {self.run.name!r}.")
        flow_artifacts_folder = self.run_output_path / f"{OutputsFolderName.FLOW_ARTIFACTS}"
        instance_results = get_instance_results(flow_artifacts_folder)
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = Local2Cloud.FLOW_INSTANCE_RESULTS_FILE_NAME
            local_file = Path(temp_dir) / file_name
            # write instance results to a temp local file
            with open(local_file, "w", encoding=DEFAULT_ENCODING) as f:
                for line_result in instance_results:
                    f.write(json.dumps(line_result) + "\n")
            remote_file = f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_ARTIFACTS}/{self.run.name}/{file_name}"
            await self._upload_local_file_to_blob(local_file, remote_file)
            return remote_file

    async def _upload_local_folder_to_blob(self, local_folder, remote_folder):
        """Upload local folder to remote folder in blob.

        Note:
            If local folder is "a/b/c", and remote folder is "x/y/z", the blob path will be "x/y/z/c".
        """
        logger.debug(f"Uploading local folder {local_folder.resolve().as_posix()!r} to blob {remote_folder!r}.")
        local_folder = Path(local_folder)

        if not local_folder.is_dir():
            raise UploadInternalError(
                f"Local folder {local_folder.resolve().as_posix()!r} does not exist or it's not a directory."
            )

        for file in local_folder.rglob("*"):
            # skip the file if it's in the ignored pattern
            skip_this_file = False
            for pattern in self.IGNORED_PATTERN:
                if pattern in file.parts:
                    skip_this_file = True
                    break
            if skip_this_file:
                continue

            # upload the file
            if file.is_file():
                # Construct the blob path
                relative_path = file.relative_to(local_folder)
                blob_path = f"{remote_folder}/{local_folder.name}/{relative_path}"
                await self._upload_local_file_to_blob(file, blob_path)

        # return the remote folder path
        return f"{remote_folder}/{local_folder.name}"

    async def _upload_local_file_to_blob(self, local_file, remote_file, target_datastore=CloudDatastore.DEFAULT):
        """Upload local file to remote file in blob."""
        local_file = Path(local_file)

        if not local_file.is_file():
            raise UploadInternalError(
                f"Local file {local_file.resolve().as_posix()!r} does not exist or it's not a file."
            )

        # choose the blob service client and container name based on the target datastore
        blob_service_client = self.blob_service_client[target_datastore]
        container_name = self.datastore[target_datastore].container_name

        # Create a blob client for the blob path
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=remote_file)
        # Upload the file to the blob
        await self._upload_single_blob(blob_client, local_file, target_datastore)

    async def _upload_single_blob(self, blob_client, data_path, target_datastore=CloudDatastore.DEFAULT) -> None:
        """Upload a single blob to cloud."""
        logger.debug(f"Uploading local file {data_path.resolve().as_posix()!r} to blob {blob_client.blob_name!r}.")
        data_path = Path(data_path)
        if not data_path.is_file():
            UploadInternalError(f"Data path {data_path.resolve().as_posix()!r} does not exist or it's not a file.")

        async with blob_client:
            with open(data_path, "rb") as f:
                try:
                    await blob_client.upload_blob(f, overwrite=self.overwrite)
                except ResourceExistsError as e:
                    error_msg = (
                        f"Failed to upload run {self.run.name!r}. Specified blob {blob_client.blob_name!r} "
                        f"already exists and overwrite is set to False. Container: {blob_client.container_name!r}. "
                        f"Datastore: {self.datastore[target_datastore].name!r}."
                    )
                    raise UploadUserError(error_msg) from e
                except HttpResponseError as e:
                    if e.status_code == 403:
                        raise UserAuthenticationError(
                            f"Failed to upload run {self.run.name!r}. "
                            f"User does not have permission to perform write operation on storage account "
                            f"{self.datastore[target_datastore].account_name!r} container "
                            f"{self.datastore[target_datastore].container_name!r}. Original azure blob error: {str(e)}"
                        )
                    raise

    @classmethod
    def _from_run_operations(cls, run: Run, run_ops: "RunOperations"):
        """Create an instance from run operations."""
        from azure.ai.ml.entities._datastore.azure_storage import AzureBlobDatastore

        datastore = run_ops._workspace_default_datastore
        if isinstance(datastore, AzureBlobDatastore):
            return cls(run=run, run_ops=run_ops)
        else:
            raise UserErrorException(
                f"Cannot upload run {run.name!r} because the workspace default datastore is not supported. "
                f"Supported ones are ['AzureBlobDatastore'], got {type(datastore).__name__!r}."
            )

    async def _check_run_details_exist_in_cloud(self, blob_path: List = None):
        """Check if run details exist in cloud, mainly for test use."""
        flow_artifacts_prefix = f"{Local2Cloud.BLOB_ROOT_PROMPTFLOW}/{Local2Cloud.BLOB_ARTIFACTS}/{self.run.name}"
        default_targets = [
            f"{flow_artifacts_prefix}/{OutputsFolderName.FLOW_ARTIFACTS}",
            f"{flow_artifacts_prefix}/{OutputsFolderName.NODE_ARTIFACTS}",
            f"{flow_artifacts_prefix}/{OutputsFolderName.FLOW_OUTPUTS}",
            f"{Local2Cloud.BLOB_EXPERIMENT_RUN}/dcid.{self.run.name}/{Local2Cloud.EXECUTION_LOG}",
            f"{Local2Cloud.BLOB_ROOT_RUNS}/{self.run.name}",
            f"{flow_artifacts_prefix}/{LocalStorageFilenames.FLOW_LOGS_FOLDER}",
            f"{flow_artifacts_prefix}/{Local2Cloud.FLOW_INSTANCE_RESULTS_FILE_NAME}",
        ]
        targets = blob_path or default_targets
        target_files = [item for item in targets if "." in Path(item).name]
        target_folders = [item for item in targets if item not in target_files]
        results = {target: False for target in targets}

        default_service_client = self.blob_service_client[CloudDatastore.DEFAULT]
        artifact_service_client = self.blob_service_client[CloudDatastore.ARTIFACT]
        async with default_service_client, artifact_service_client:
            default_container_client = default_service_client.get_container_client(
                self.datastore[CloudDatastore.DEFAULT].container_name
            )
            artifact_container_client = artifact_service_client.get_container_client(
                self.datastore[CloudDatastore.ARTIFACT].container_name
            )
            async with default_container_client, artifact_container_client:
                # check blob existence
                for target in target_files:
                    container_client = (
                        default_container_client
                        if not target.endswith(Local2Cloud.EXECUTION_LOG)
                        else artifact_container_client
                    )
                    blob_client = container_client.get_blob_client(target)
                    if await blob_client.exists():
                        results[target] = True

                # check folder existence
                for target in target_folders:
                    # all folder targets should be in default container
                    async for _ in default_container_client.list_blobs(name_starts_with=target):
                        results[target] = True
                        break
        return results
