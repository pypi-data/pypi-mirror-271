import collections.abc
import dataclasses
from functools import partial
import importlib.metadata
import os
import pathlib
import typing

import pathspec

from roboto.env import default_env

from ...auth import Permissions
from ...exceptions import (
    RobotoInvalidRequestException,
    RobotoNotFoundException,
)
from ...logging import default_logger
from ...query import QuerySpecification
from ...serde import (
    exclude_patterns_to_spec,
    pydantic_jsonable_dict,
)
from ...transactions import (
    TransactionManagerABC,
    TransactionRecord,
    TransactionType,
)
from ...updates import (
    MetadataChangeset,
    StrSequence,
    UpdateCondition,
)
from ..files import (
    File,
    FileDelegate,
    FileRecord,
    FileTag,
    S3Credentials,
)
from ..files.progress import (
    TqdmProgressMonitorFactory,
)
from .delegate import (
    Credentials,
    DatasetDelegate,
    StorageLocation,
)
from .record import Administrator, DatasetRecord

logger = default_logger()


@dataclasses.dataclass
class FileUploadInfo:
    bucket: str
    key: str
    transaction_id: str


class Dataset:
    __dataset_delegate: DatasetDelegate
    __file_delegate: FileDelegate
    __record: DatasetRecord
    __temp_credentials: typing.Optional[Credentials] = None
    __transaction_manager: TransactionManagerABC

    @classmethod
    def create(
        cls,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
        transaction_manager: TransactionManagerABC,
        administrator: Administrator = Administrator.Roboto,
        storage_location: StorageLocation = StorageLocation.S3,
        org_id: typing.Optional[str] = None,
        created_by: typing.Optional[str] = None,
        metadata: typing.Optional[dict[str, typing.Any]] = None,
        tags: typing.Optional[list[str]] = None,
        description: typing.Optional[str] = None,
    ) -> "Dataset":
        record = dataset_delegate.create_dataset(
            administrator,
            metadata,
            storage_location,
            tags,
            org_id,
            created_by,
            description,
        )
        return cls(record, dataset_delegate, file_delegate, transaction_manager)

    @classmethod
    def from_id(
        cls,
        dataset_id: str,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
        transaction_manager: TransactionManagerABC,
    ) -> "Dataset":
        record = dataset_delegate.get_dataset_by_id(dataset_id)
        return cls(record, dataset_delegate, file_delegate, transaction_manager)

    @classmethod
    def query(
        cls,
        query: QuerySpecification,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
        transaction_manager: TransactionManagerABC,
        org_id: typing.Optional[str] = None,
    ) -> collections.abc.Generator["Dataset", None, None]:
        known = set(DatasetRecord.model_fields.keys())
        actual = set()
        for field in query.fields():
            # Support dot notation for nested fields
            # E.g., "metadata.SoftwareVersion"
            if "." in field:
                actual.add(field.split(".")[0])
            else:
                actual.add(field)
        unknown = actual - known
        if unknown:
            plural = len(unknown) > 1
            msg = (
                "are not known attributes of Dataset"
                if plural
                else "is not a known attribute of Dataset"
            )
            raise ValueError(f"{unknown} {msg}. Known attributes: {known}")

        paginated_results = dataset_delegate.query_datasets(query, org_id=org_id)
        while True:
            for record in paginated_results.items:
                yield cls(record, dataset_delegate, file_delegate, transaction_manager)
            if paginated_results.next_token:
                query.after = paginated_results.next_token
                paginated_results = dataset_delegate.query_datasets(
                    query, org_id=org_id
                )
            else:
                break

    def __init__(
        self,
        record: DatasetRecord,
        dataset_delegate: DatasetDelegate,
        file_delegate: FileDelegate,
        transaction_manager: TransactionManagerABC,
    ) -> None:
        self.__dataset_delegate = dataset_delegate
        self.__file_delegate = file_delegate
        self.__record = record
        self.__transaction_manager = transaction_manager

    @property
    def dataset_id(self) -> str:
        return self.__record.dataset_id

    @property
    def metadata(self) -> dict[str, typing.Any]:
        return self.__record.metadata.copy()

    @property
    def record(self) -> DatasetRecord:
        return self.__record

    @property
    def tags(self) -> list[str]:
        return self.__record.tags.copy()

    def delete_dataset(self) -> None:
        self.__dataset_delegate.delete_dataset(self.__record)

    def delete_files(
        self,
        include_patterns: typing.Optional[list[str]] = None,
        exclude_patterns: typing.Optional[list[str]] = None,
    ) -> None:
        """
        Delete files associated with this dataset.

        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.delete_files(
            ...    include_patterns=["**/*.png"],
            ...    exclude_patterns=["**/back_camera/**"]
            ... )

        """
        for file in self.list_files(include_patterns, exclude_patterns):
            file.delete()

    def download_files(
        self,
        out_path: pathlib.Path,
        include_patterns: typing.Optional[list[str]] = None,
        exclude_patterns: typing.Optional[list[str]] = None,
    ) -> None:
        """
        Download files associated with this dataset to the given directory.
        If `out_path` does not exist, it will be created.

        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.download_files(
            ...     pathlib.Path("/tmp/tmp.nV1gdW5WHV"),
            ...     include_patterns=["**/*.g4"],
            ...     exclude_patterns=["**/test/**"]
            ... )
        """
        if (
            self.__record.storage_location != StorageLocation.S3
            or self.__record.administrator != Administrator.Roboto
        ):
            raise NotImplementedError(
                "Only S3-backed storage administered by Roboto is supported at this time."
            )

        if not out_path.is_dir():
            out_path.mkdir(parents=True)

        def _credential_provider():
            return self.get_temporary_credentials(
                Permissions.ReadOnly
            ).to_s3_credentials()

        def _file_to_download_tuple(f: File) -> tuple[FileRecord, pathlib.Path]:
            return f.record, out_path / f.relative_path

        all_files = list(self.list_files(include_patterns, exclude_patterns))

        def _file_generator():
            for x in map(
                _file_to_download_tuple,
                all_files,
            ):
                yield x

        self.__file_delegate.download_files(
            file_generator=_file_generator(),
            credential_provider=_credential_provider,
            progress_monitor_factory=TqdmProgressMonitorFactory(
                concurrency=1,
                ctx={
                    "base_path": self.__record.dataset_id,
                    "total_file_count": len(all_files),
                },
            ),
            max_concurrency=8,
        )

    def get_file_info(
        self,
        relative_path: typing.Union[str, pathlib.Path],
    ) -> File:
        """
        Get a File object for the given relative path.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> file = dataset.get_file_info("foo/bar.txt")
            >>> print(file.file_id)
            file-abc123
        """
        matching = list(self.list_files(include_patterns=[str(relative_path)]))
        if not matching:
            raise RobotoNotFoundException(
                f"File '{relative_path}' not found in dataset '{self.dataset_id}'"
            )

        if len(matching) > 1:
            raise RobotoInvalidRequestException(
                f"Multiple files found for '{relative_path}' in dataset '{self.dataset_id}'"
            )

        return matching[0]

    def get_temporary_credentials(
        self,
        permissions: Permissions = Permissions.ReadOnly,
        caller: typing.Optional[str] = None,  # A Roboto user_id
        force_refresh: bool = False,
        transaction_id: typing.Optional[str] = None,
    ) -> Credentials:
        if (
            force_refresh
            or permissions == Permissions.ReadWrite
            or self.__temp_credentials is None
            or self.__temp_credentials.is_expired()
        ):
            self.__temp_credentials = self.__dataset_delegate.get_temporary_credentials(
                self.__record, permissions, caller, transaction_id
            )
        return self.__temp_credentials

    def list_files(
        self,
        include_patterns: typing.Optional[list[str]] = None,
        exclude_patterns: typing.Optional[list[str]] = None,
    ) -> collections.abc.Generator[File, None, None]:
        """
        List files associated with this dataset.

        `include_patterns` and `exclude_patterns` are lists of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> for file in dataset.list_files(
            ...     include_patterns=["**/*.g4"],
            ...     exclude_patterns=["**/test/**"]
            ... ):
            ...     print(file.relative_path)
        """

        paginated_results = self.__dataset_delegate.list_files(
            self.__record.dataset_id,
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
        )
        while True:
            for record in paginated_results.items:
                yield File(record, self.__file_delegate)
            if paginated_results.next_token:
                paginated_results = self.__dataset_delegate.list_files(
                    self.__record.dataset_id,
                    paginated_results.next_token,
                    include_patterns=include_patterns,
                    exclude_patterns=exclude_patterns,
                )
            else:
                break

    def put_metadata(
        self,
        metadata: dict[str, typing.Any],
        updated_by: typing.Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """
        Set each `key`: `value` in this dict as dataset metadata if it doesn't exist, else overwrite the existing value.
        Keys must be strings. Dot notation is supported for nested keys.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.put_metadata({
            ...     "foo": "bar",
            ...     "baz.qux": 101,
            ... })

        """
        self.update(
            metadata_changeset=MetadataChangeset(put_fields=metadata),
            updated_by=updated_by,
        )

    def put_tags(
        self,
        tags: StrSequence,
        updated_by: typing.Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """Add each tag in this sequence if it doesn't exist"""
        self.update(
            metadata_changeset=MetadataChangeset(put_tags=tags),
            updated_by=updated_by,
        )

    def refresh(self) -> None:
        """Refresh the underlying dataset record with the latest server state."""
        self.__record = self.__dataset_delegate.get_dataset_by_id(
            self.__record.dataset_id
        )

    def remove_metadata(
        self,
        metadata: StrSequence,
        updated_by: typing.Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """
        Remove each key in this sequence from dataset metadata if it exists.
        Keys must be strings. Dot notation is supported for nested keys.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.remove_metadata(["foo", "baz.qux"])
        """
        self.update(
            metadata_changeset=MetadataChangeset(remove_fields=metadata),
            updated_by=updated_by,
        )

    def remove_tags(
        self,
        tags: StrSequence,
        updated_by: typing.Optional[str] = None,  # A Roboto user_id
    ) -> None:
        """Remove each tag in this sequence if it exists"""
        self.update(
            metadata_changeset=MetadataChangeset(remove_tags=tags),
            updated_by=updated_by,
        )

    def to_dict(self) -> dict[str, typing.Any]:
        return pydantic_jsonable_dict(self.__record)

    def upload_directory(
        self,
        directory_path: pathlib.Path,
        exclude_patterns: typing.Optional[list[str]] = None,
        timeout: int = 300,
    ) -> None:
        """
        Upload everything, recursively, in directory, ignoring files that match any of the ignore patterns.

        `exclude_patterns` is a list of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore#_pattern_format.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.upload_directory(
            ...     pathlib.Path("/path/to/directory"),
            ...     exclude_patterns=[
            ...         "__pycache__/",
            ...         "*.pyc",
            ...         "node_modules/",
            ...         "**/*.log",
            ...     ],
            ... )
        """
        return self.upload_file_directory(directory_path, exclude_patterns)

    def upload_file_directory(
        self,
        directory_path: pathlib.Path,
        exclude_patterns: typing.Optional[list[str]] = None,
    ) -> None:
        """
        Upload everything, recursively, in directory, ignoring files that match any of the ignore patterns.

        `exclude_patterns` is a list of gitignore-style patterns.
        See https://git-scm.com/docs/gitignore#_pattern_format.

        Example:
            >>> from roboto.domain import datasets
            >>> dataset = datasets.Dataset(...)
            >>> dataset.upload_directory(
            ...     pathlib.Path("/path/to/directory"),
            ...     exclude_patterns=[
            ...         "__pycache__/",
            ...         "*.pyc",
            ...         "node_modules/",
            ...         "**/*.log",
            ...     ],
            ... )
        """
        exclude_spec: typing.Optional[pathspec.PathSpec] = exclude_patterns_to_spec(
            exclude_patterns
        )
        all_files = _list_directory_files(directory_path, exclude_spec=exclude_spec)
        file_destination_paths = {
            path: os.path.relpath(path, directory_path) for path in all_files
        }

        return self.upload_files(all_files, file_destination_paths)

    def upload_files(
        self,
        files: collections.abc.Iterable[pathlib.Path],
        file_destination_paths: dict[pathlib.Path, str] = {},
    ):
        package_version = importlib.metadata.version("roboto")
        origination = default_env.roboto_env or f"roboto {package_version}"
        file_manifest = {
            file_destination_paths.get(path, path.name): path.stat().st_size
            for path in files
        }
        total_file_count = len(file_manifest)
        total_file_size = sum(file_manifest.values())

        begin_response = self.__transaction_manager.begin_manifest_transaction(
            resource_manifest=file_manifest,
            origination=origination,
            dataset_id=self.__record.dataset_id,
            org_id=self.__record.org_id,
            resource_owner_id=self.__record.org_id,
        )
        transaction = begin_response.record
        logger.debug("Transaction id: %s", transaction.transaction_id)

        file_path_to_manifest_mappings = {
            file_destination_paths.get(path, path.name): path for path in files
        }
        upload_mappings = {
            file_path_to_manifest_mappings[src_path]: dest_uri
            for src_path, dest_uri in begin_response.upload_mappings.items()
        }
        logger.debug("Upload mappings: %s", upload_mappings)

        progress_monitor_factory = TqdmProgressMonitorFactory(
            concurrency=1,
            ctx={
                "expected_file_count": total_file_count,
                "expected_file_size": total_file_size,
            },
        )

        with progress_monitor_factory.upload_monitor(
            source=f"{total_file_count} file" + ("s" if total_file_count != 1 else ""),
            size=total_file_size,
        ) as progress_monitor:
            self.__file_delegate.upload_many_files(
                file_generator=upload_mappings.items(),
                credential_provider=partial(
                    self.__credential_provider, transaction.transaction_id
                ),
                on_file_complete=partial(
                    self.__transaction_manager.on_manifest_item_complete,
                    self.__record.dataset_id,
                    transaction.transaction_id,
                ),
                progress_monitor=progress_monitor,
                max_concurrency=8,
            )

        self.__transaction_manager.complete_manifest_transaction(
            dataset_id=self.__record.dataset_id,
            transaction_id=transaction.transaction_id,
            org_id=self.__record.org_id,
            resource_owner_id=self.__record.org_id,
        )

    def __credential_provider(self, transaction_id: str):
        return self.get_temporary_credentials(
            Permissions.ReadWrite,
            force_refresh=True,
            transaction_id=transaction_id,
        ).to_s3_credentials()

    def upload_file(
        self,
        local_file_path: pathlib.Path,
        key: str,
        credentials: typing.Optional[Credentials] = None,
        credential_provider: typing.Optional[typing.Callable[[], S3Credentials]] = None,
    ) -> FileUploadInfo:
        """
        Uploads a single file to the dataset's storage location.
        """
        self.upload_files([local_file_path], {local_file_path: key})

        files = self.list_files(include_patterns=[key])
        file_record = next(files).record

        return FileUploadInfo(
            bucket=file_record.bucket,
            key=file_record.key,
            transaction_id=file_record.upload_id,
        )

    def update(
        self,
        metadata_changeset: typing.Optional[MetadataChangeset] = None,
        conditions: typing.Optional[list[UpdateCondition]] = None,
        description: typing.Optional[str] = None,
        updated_by: typing.Optional[str] = None,  # A Roboto user_id
    ) -> None:
        updated = self.__dataset_delegate.update(
            self.__record,
            metadata_changeset=metadata_changeset,
            conditions=conditions,
            description=description,
            updated_by=updated_by,
        )
        self.__record = updated

    def __start_transaction(
        self,
        expected_file_count: int,
    ) -> TransactionRecord:
        package_version = importlib.metadata.version("roboto")
        origination = default_env.roboto_env or f"roboto {package_version}"
        return self.__transaction_manager.begin_transaction(
            transaction_type=TransactionType.FileUpload,
            origination=origination,
            expected_resource_count=expected_file_count,
            org_id=self.__record.org_id,
            resource_owner_id=self.__record.org_id,
        )

    def __upload_file(
        self,
        local_file_path: pathlib.Path,
        key: str,
        transaction_id: str,
        credentials: typing.Optional[Credentials] = None,
        credential_provider: typing.Optional[typing.Callable[[], S3Credentials]] = None,
    ) -> FileUploadInfo:
        """
        Uploads a file to the dataset's storage location. Does not mark the upload as complete.
        """
        if not local_file_path.is_file():
            raise ValueError(f"{local_file_path} is not a file")

        if (
            self.__record.storage_location != StorageLocation.S3
            or self.__record.administrator != Administrator.Roboto
        ):
            raise NotImplementedError(
                "Only S3-backed storage administered by Roboto is supported at this time."
            )

        credentials = (
            credentials
            if credentials is not None
            else self.get_temporary_credentials(
                Permissions.ReadWrite, transaction_id=transaction_id
            )
        )

        if credential_provider is None:

            def _credential_provider():
                return self.get_temporary_credentials(
                    Permissions.ReadWrite, transaction_id=transaction_id
                ).to_s3_credentials()

            credential_provider = _credential_provider

        key = f"{credentials.required_prefix}/{key.lstrip('/')}"
        self.__file_delegate.upload_file(
            local_file_path,
            credentials.bucket,
            key,
            credential_provider,
            tags={
                FileTag.DatasetId: self.__record.dataset_id,
                FileTag.OrgId: self.__record.org_id,
                FileTag.CommonPrefix: credentials.required_prefix,
                FileTag.TransactionId: transaction_id,
            },
            progress_monitor_factory=TqdmProgressMonitorFactory(concurrency=1),
        )

        return FileUploadInfo(
            bucket=credentials.bucket,
            key=key,
            transaction_id=transaction_id,
        )


def _list_directory_files(
    directory_path: pathlib.Path,
    exclude_spec: typing.Optional[pathspec.PathSpec] = None,
) -> collections.abc.Iterable[pathlib.Path]:
    all_files = set()

    for root, _, files in os.walk(directory_path):
        for file in files:
            if not exclude_spec or not exclude_spec.match_file(file):
                all_files.add(pathlib.Path(root, file))

    return all_files
