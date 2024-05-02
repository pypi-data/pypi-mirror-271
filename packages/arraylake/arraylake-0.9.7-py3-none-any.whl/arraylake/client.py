"""
The Client module contains the main classes used to interact with the Arraylake service.
For asyncio interaction, use the #AsyncClient. For regular, non-async interaction, use the #Client.

**Example usage:**

```python
from arraylake import Client
client = Client()
repo = client.get_repo("my-org/my-repo")
```
"""

import re
import warnings
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Literal, Optional
from urllib.parse import urlparse
from uuid import UUID

from arraylake.asyn import sync
from arraylake.chunkstore import (
    Chunkstore,
    mk_chunkstore_from_bucket_config,
    mk_chunkstore_from_uri,
)
from arraylake.config import config
from arraylake.exceptions import BucketNotFoundError
from arraylake.log_util import get_logger
from arraylake.metastore import HttpMetastore, HttpMetastoreConfig
from arraylake.repo import AsyncRepo, Repo
from arraylake.types import DBID, Author, BucketResponse, NewBucket
from arraylake.types import Repo as RepoModel
from arraylake.types import RepoOperationMode, RepoOperationStatusResponse

logger = get_logger(__name__)

_VALID_NAME = r"(\w[\w\.\-_]+)"


def _parse_org_and_repo(org_and_repo: str) -> tuple[str, str]:
    expr = f"{_VALID_NAME}/{_VALID_NAME}"
    res = re.fullmatch(expr, org_and_repo)
    if not res:
        raise ValueError(f"Not a valid repo identifier: `{org_and_repo}`. " "Should have the form `[ORG]/[REPO]`.")
    org, repo_name = res.groups()
    return org, repo_name


def _validate_org(org_name: str):
    if not re.fullmatch(_VALID_NAME, org_name):
        raise ValueError(f"Invalid org name: `{org_name}`.")


def _default_service_uri() -> str:
    return config.get("service.uri", "https://api.earthmover.io")


def _default_token() -> Optional[str]:
    return config.get("token", None)


@dataclass
class AsyncClient:
    """Asyncio Client for interacting with ArrayLake

    Args:
        service_uri (str): [Optional] The service URI to target.
        token (str): [Optional] API token for service account authentication.
    """

    service_uri: str = field(default_factory=_default_service_uri)
    token: Optional[str] = field(default_factory=_default_token, repr=False)
    auth_org: Optional[str] = None

    def __post_init__(self):
        if self.token is not None and not self.token.startswith("ema_"):
            raise ValueError("Invalid token provided. Tokens must start with ema_")
        if not self.service_uri.startswith("http"):
            raise ValueError("service uri must start with http")
        self.auth_org = self.auth_org or config.get("user.org", None)

    def _metastore_for_org(self, org: str) -> HttpMetastore:
        _validate_org(org)
        return HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))

    async def list_repos(self, org: str) -> Sequence[RepoModel]:
        """List all repositories for the specified org

        Args:
            org: Name of the org
        """

        mstore = self._metastore_for_org(org)
        repos = await mstore.list_databases()
        return repos

    def _init_chunkstore(self, repo_id: DBID, bucket: Optional[BucketResponse]) -> Chunkstore:
        inline_threshold_bytes = int(config.get("chunkstore.inline_threshold_bytes", 0))
        if bucket is None:
            chunkstore_uri = config.get("chunkstore.uri")
            if chunkstore_uri is None:
                raise ValueError("Chunkstore uri is None. Please set it using: `arraylake config set chunkstore.uri URI`.")
            if chunkstore_uri.startswith("s3"):
                client_kws = config.get("s3", {})
            elif chunkstore_uri.startswith("gs"):
                client_kws = config.get("gs", {})
            else:
                raise ValueError(f"Unsupported chunkstore uri: {chunkstore_uri}")
            return mk_chunkstore_from_uri(chunkstore_uri, inline_threshold_bytes, **client_kws)
        else:
            # TODO: for now, we just punt and use the s3 namespace for server-managed
            # bucket configs. This should be generalized to support GCS.
            client_kws = config.get("s3", {})
            return mk_chunkstore_from_bucket_config(bucket, repo_id, inline_threshold_bytes, **client_kws)

    async def get_repo_object(self, name: str):
        """Get the repo configuration object.

        See `get_repo` for an instantiated repo including chunkstore.
        """
        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)

        # This is non-optimal because open_database will list_databases again
        repos = [repo for repo in await mstore.list_databases() if repo.name == repo_name]
        if len(repos) != 1:
            raise ValueError(f"Cannot find repo `{name}`.")
        return repos[0]

    async def get_repo(self, name: str, *, checkout: bool = True) -> AsyncRepo:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            checkout: Automatically checkout the repo after instantiation.
        """
        org, repo_name = _parse_org_and_repo(name)
        repo = await self.get_repo_object(name)
        mstore = HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token, self.auth_org))

        db = await mstore.open_database(repo_name)
        cstore = self._init_chunkstore(repo.id, repo.bucket)

        user = await mstore.get_user()

        author: Author = user.as_author()
        arepo = AsyncRepo(db, cstore, name, author)
        if checkout:
            await arepo.checkout()
        return arepo

    async def _set_repo_status(
        self, qualified_repo_name: str, mode: RepoOperationMode, message: str | None = None
    ) -> RepoOperationStatusResponse:
        org, repo_name = _parse_org_and_repo(qualified_repo_name)
        mstore = self._metastore_for_org(org)
        return await mstore.set_repo_status(repo_name, mode, message)

    async def get_or_create_repo(
        self,
        name: str,
        bucket_nickname: Optional[str] = None,
        *,
        checkout: bool = True,
        bucket_config_nickname: Optional[str] = None,
    ) -> AsyncRepo:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            bucket_config_nickname: the created repo will use this bucket for its chunks.
               If the repo exists, bucket_config_nickname is ignored.
            checkout: Automatically checkout the repo after instantiation.
               If the repo does not exist, checkout is ignored.
        """
        if bucket_config_nickname is None and bucket_nickname:
            bucket_config_nickname = bucket_nickname
            warnings.warn("bucket_nickname has been renamed to bucket_config_nickname and will be removed in Arraylake 0.10", FutureWarning)
        org, repo_name = _parse_org_and_repo(name)
        repos = [r for r in await self.list_repos(org) if r.name == repo_name]
        if repos:
            (repo,) = repos
            if bucket_config_nickname:
                if repo.bucket and bucket_config_nickname != repo.bucket.nickname:
                    # NOTE: mypy complains about line length, so we break up the string here.
                    start_string = f"This repo exists, but the provided {bucket_config_nickname=}"
                    end_string = f"does not match the configured bucket_config_nickname {repo.bucket.nickname!r}."
                    error_string = f"{start_string} {end_string}"
                    raise ValueError(error_string)
                elif not repo.bucket:
                    raise ValueError(
                        "This repo exists, but does not have a bucket config attached. Please remove the bucket_config_nickname argument."
                    )
                else:
                    return await self.get_repo(name, checkout=checkout)
            return await self.get_repo(name, checkout=checkout)
        else:
            return await self.create_repo(name, bucket_config_nickname=bucket_config_nickname)

    async def create_repo(
        self,
        name: str,
        bucket_nickname: Optional[str] = None,
        *,
        bucket_config_nickname: Optional[str] = None,
    ) -> AsyncRepo:
        """Create a new repo

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO])
            bucket_config_nickname: An optional bucket to use for the chunkstore
        """
        if bucket_config_nickname is None and bucket_nickname:
            bucket_config_nickname = bucket_nickname
            warnings.warn("bucket_nickname has been renamed to bucket_config_nickname and will be removed in Arraylake 0.10", FutureWarning)

        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)
        db = await mstore.create_database(repo_name, bucket_config_nickname)

        repos = [repo for repo in await mstore.list_databases() if repo.name == repo_name]
        if len(repos) != 1:
            raise ValueError(f"Error creating repository `{name}`.")
        repo = repos[0]

        cstore = self._init_chunkstore(repo.id, repo.bucket)
        user = await mstore.get_user()
        author: Author = user.as_author()

        arepo = AsyncRepo(db, cstore, name, author)
        await arepo.checkout()
        return arepo

    async def delete_repo(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form [ORG]/[REPO])
            imsure, imreallysure: confirm you intend to delete this bucket config
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)
        await mstore.delete_database(repo_name, imsure=imsure, imreallysure=imreallysure)

    async def _bucket_id_for_nickname(self, mstore: HttpMetastore, nickname: str) -> UUID:
        buckets = await mstore.list_bucket_configs()
        bucket_id = next((b.id for b in buckets if b.nickname == nickname), None)
        if not bucket_id:
            raise BucketNotFoundError(nickname)
        return bucket_id

    def _make_bucket_config(self, *, nickname: str, uri: str, extra_config: dict | None, auth_config: dict | None) -> dict:
        if not nickname:
            raise ValueError("nickname must be specified if uri is provided.")

        # unpack optionals
        if extra_config is None:
            extra_config = {}
        if auth_config is None:
            auth_config = {"method": "anonymous"}

        # parse uri and get prefix
        res = urlparse(uri)
        platform: Literal["s3", "gs", "s3-compatible"] | None = "s3" if res.scheme == "s3" else "gs" if res.scheme == "gs" else None
        if platform == "s3" and extra_config.get("endpoint_url"):
            platform = "s3-compatible"
        if platform not in ["s3", "gs", "s3-compatible"]:
            raise ValueError(f"Invalid platform {platform} for uri {uri}")
        name = res.netloc
        prefix = res.path[1:] if res.path.startswith("/") else res.path  # is an empty string if not specified

        if "method" not in auth_config or auth_config["method"] not in ["customer_managed_role", "bucket_policy", "hmac", "anonymous"]:
            raise ValueError("invalid auth_config, must provide method key of customer_managed_role, bucket_policy, hmac, or anonymous")

        return dict(
            platform=platform,
            name=name,
            prefix=prefix,
            nickname=nickname,
            extra_config=extra_config,
            auth_config=auth_config,
        )

    async def create_bucket_config(
        self, *, org: str, nickname: str, uri: str, extra_config: dict | None = None, auth_config: dict | None = None
    ) -> BucketResponse:
        """Create a new bucket config entry

        NOTE: This does not create any actual buckets in the object store.

        Args:
            org: Name of the org
            nickname: bucket nickname (example: ours3-bucket`)
            uri: The URI of the object store, of the form
                platform://bucket_name[/prefix].
            extra_config: dictionary of additional config to set on bucket config
            auth_config: dictionary of auth parameters, must include "method" key, default is `{"method": "anonymous"}`
        """
        validated = NewBucket(**self._make_bucket_config(nickname=nickname, uri=uri, extra_config=extra_config, auth_config=auth_config))
        mstore = self._metastore_for_org(org)
        bucket = await mstore.create_bucket_config(validated)
        return bucket

    async def set_default_bucket_config(self, *, org: str, nickname: str) -> None:
        """Set the organization's default bucket for any new repos

        Args:
            nickname: Nickname of the bucket config to set as default.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        await mstore.set_default_bucket_config(bucket_id)

    async def get_bucket_config(self, *, org: str, nickname: str) -> BucketResponse:
        """Get a bucket's configuration

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to retrieve.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        bucket = await mstore.get_bucket_config(bucket_id)
        return bucket

    async def list_bucket_configs(self, org: str) -> list[BucketResponse]:
        """List all bucket config entries

        Args:
            org: Name of the organization.
        """
        mstore = self._metastore_for_org(org)
        return await mstore.list_bucket_configs()

    async def list_repos_for_bucket_config(self, *, org: str, nickname: str) -> list[RepoModel]:
        """List repos using a given bucket

        Args:
            org: Name of the org
            nickname: Nickname of the bucket configuration.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        buckets = await mstore.list_repos_for_bucket_config(bucket_id)
        return buckets

    async def delete_bucket_config(self, *, org: str, nickname: str, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a bucket config entry

        NOTE: If a bucket config is in use by one or more repos, it cannot be
        deleted. This does not actually delete any buckets in the object store.

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to delete.
            imsure, imreallysure: confirm you intend to delete this bucket config
        """
        if not (imsure and imreallysure):
            raise ValueError("imsure and imreallysure must be set to True")
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        await mstore.delete_bucket_config(bucket_id)


@dataclass
class Client:
    """Client for interacting with ArrayLake.

    Args:
        service_uri (str): [Optional] The service URI to target.
        token (str): [Optional] API token for service account authentication.
    """

    service_uri: Optional[str] = None
    token: Optional[str] = field(default=None, repr=False)
    auth_org: Optional[str] = None

    def __post_init__(self):
        if self.token is None:
            self.token = config.get("token", None)
        if self.service_uri is None:
            self.service_uri = config.get("service.uri")
        self.auth_org = self.auth_org or config.get("user.org", None)

        self.aclient = AsyncClient(self.service_uri, token=self.token, auth_org=self.auth_org)

    def list_repos(self, org: str) -> Sequence[RepoModel]:
        """List all repositories for the specified org

        Args:
            org: Name of the org
        """

        repo_list = sync(self.aclient.list_repos, org)
        return repo_list

    def get_repo(self, name: str, *, checkout: bool = True) -> Repo:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            checkout: Automatically checkout the repo after instantiation.
        """

        arepo = sync(self.aclient.get_repo, name, checkout=checkout)
        return Repo(arepo)

    def get_or_create_repo(
        self, name: str, bucket_nickname: Optional[str] = None, *, checkout: bool = True, bucket_config_nickname: Optional[str] = None
    ) -> Repo:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            bucket_config_nickname: the created repo will use this bucket config for its chunks.
               If the repo exists, bucket_config_nickname is ignored.
            checkout: Automatically checkout the repo after instantiation.
               If the repo does not exist, checkout is ignored.
        """
        arepo = sync(
            self.aclient.get_or_create_repo,
            name,
            bucket_config_nickname=bucket_config_nickname,
            bucket_nickname=bucket_nickname,
            checkout=checkout,
        )
        return Repo(arepo)

    def create_repo(self, name: str, bucket_nickname: Optional[str] = None, *, bucket_config_nickname: Optional[str] = None) -> Repo:
        """Create a new repo

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO])
            bucket_config_nickname: An optional bucket to use for the chunkstore
        """

        arepo = sync(self.aclient.create_repo, name, bucket_config_nickname=bucket_config_nickname, bucket_nickname=bucket_nickname)
        return Repo(arepo)

    def delete_repo(self, name: str, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form [ORG]/[REPO])
        """

        return sync(self.aclient.delete_repo, name, imsure=imsure, imreallysure=imreallysure)

    def create_bucket_config(
        self, *, org: str, nickname: str, uri: str, extra_config: dict | None = None, auth_config: dict | None = None
    ) -> BucketResponse:
        """Create a new bucket config entry

        NOTE: This does not create any actual buckets in the object store.

        Args:
            org: Name of the org
            nickname: bucket nickname (example: our-s3-bucket)
            uri: The URI of the object store, of the form
                platform://bucket_name[/prefix].
            extra_config: dictionary of additional config to set on bucket config
            auth_config: dictionary of auth parameters, must include "method" key, default is `{"method": "anonymous"}`
        """
        return sync(
            self.aclient.create_bucket_config, org=org, nickname=nickname, uri=uri, extra_config=extra_config, auth_config=auth_config
        )

    def set_default_bucket_config(self, *, org: str, nickname: str) -> None:
        """Set the organization's default bucket config for any new repos

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to set as default.
        """
        return sync(self.aclient.set_default_bucket_config, org=org, nickname=nickname)

    def get_bucket_config(self, *, org: str, nickname: str) -> BucketResponse:
        """Get a bucket's configuration

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to retrieve.
        """
        return sync(self.aclient.get_bucket_config, org=org, nickname=nickname)

    def list_bucket_configs(self, org: str) -> list[BucketResponse]:
        """List all buckets for the specified org

        Args:
            org: Name of the org
        """
        return sync(self.aclient.list_bucket_configs, org)

    def list_repos_for_bucket_config(self, *, org: str, nickname: str) -> list[Repo]:
        """List repos using a given bucket config

        Args:
            org: Name of the org
            nickname: Nickname of the bucket.
        """
        return sync(self.aclient.list_repos_for_bucket_config, org=org, nickname=nickname)

    def delete_bucket_config(self, *, org: str, nickname: str, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a bucket config entry

        NOTE: If a bucket config is in use by one or more repos, it cannot be
        deleted. This does not actually delete any buckets in the object store.

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to delete.
            imsure, imreallysure: confirm you intend to delete this bucket config
        """
        return sync(self.aclient.delete_bucket_config, org=org, nickname=nickname, imsure=imsure, imreallysure=imreallysure)
