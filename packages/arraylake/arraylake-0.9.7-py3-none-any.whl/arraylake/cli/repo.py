import warnings
from enum import Enum
from typing import Optional

import typer
from rich import print_json
from rich.table import Table

from arraylake import AsyncClient
from arraylake.cli.utils import coro, rich_console, simple_progress
from arraylake.log_util import get_logger
from arraylake.types import RepoOperationMode

app = typer.Typer(help="Manage Arraylake repositories", no_args_is_help=True)
logger = get_logger(__name__)


class ListOutputType(str, Enum):
    rich = "rich"
    json = "json"


def _repos_table(repos, org):
    table = Table(title=f"Arraylake Repositories for [bold]{org}[/bold]", min_width=80)
    table.add_column("Name", justify="left", style="cyan", no_wrap=True, min_width=45)
    table.add_column("Created", justify="right", style="green", min_width=25)
    table.add_column("Updated", justify="right", style="green", min_width=25)
    table.add_column("Status", justify="right", style="green", min_width=25)

    mode_colors = {"online": "green", "maintenance": "yellow", "offline": "red"}

    for repo in repos:
        table.add_row(repo.name, repo.created.isoformat(), repo.updated.isoformat(), repo.status.mode, style=mode_colors[repo.status.mode])

    return table


@app.command(name="list")
@coro  # type: ignore
async def list_repos(
    org: str = typer.Argument(..., help="The organization name"), output: ListOutputType = typer.Option("rich", help="Output formatting")
):
    """**List** repositories in the specified organization

    **Examples**

    - List repos in _default_ org

        ```
        $ arraylake repo list my-org
        ```
    """
    with simple_progress(f"Listing repos for [bold]{org}[/bold]...", quiet=(output != "rich")):
        repos = await AsyncClient().list_repos(org)

    if output == "json":
        repos = [r._asdict() for r in repos]
        print_json(data=repos)
    elif repos:
        rich_console.print(_repos_table(repos, org))
    else:
        rich_console.print("\nNo results")


@app.command()
@coro  # type: ignore
async def create(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    bucket_config_nickname: Optional[str] = typer.Option(None, help="Chunkstore bucket config nickname"),
    bucket_nickname: Optional[str] = typer.Option(None, help="Chunkstore bucket config nickname (DEPRECATED)"),
):
    """**Create** a new repository

    **Examples**

    - Create new repository

        ```
        $ arraylake repo create my-org/example-repo --bucket-config-nickname arraylake-bucket
        ```
    """
    if bucket_nickname:
        bucket_config_nickname = bucket_nickname
        warnings.warn("bucket-nickname has been renamed to bucket-config-nickname and will be removed in Arraylake 0.10", FutureWarning)
    with simple_progress(f"Creating repo [bold]{repo_name}[/bold]..."):
        await AsyncClient().create_repo(repo_name, bucket_config_nickname=bucket_config_nickname)


@app.command()
@coro  # type: ignore
async def delete(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    confirm: bool = typer.Option(False, help="confirm deletion without prompting"),
):
    """**Delete** a repository

    **Examples**

    - Delete repository without confirmation prompt

        ```
        $ arraylake repo delete my-org/example-repo --confirm
        ```
    """
    if not confirm:
        confirm = typer.confirm(f"This will permanently remove the {repo_name} repo. Are you sure you want to continue?", abort=True)

    with simple_progress(f"Deleting repo [bold]{repo_name}[/bold]..."):
        await AsyncClient().delete_repo(repo_name, imsure=confirm, imreallysure=confirm)


@app.command()
@coro  # type: ignore
async def tree(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    depth: int = typer.Option(10, help="Maximum depth to descend into hierarchy."),
    prefix: str = typer.Option("", help="Path in repo to start the hierarchy, e.g. `root/foo`."),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    """Show tree representation of a repository

    **Examples**

    - Show the tree representation of a repo up to level 5

        ```
        $ arraylake repo tree my-org/example-repo --depth 5
        ```
    """

    client = AsyncClient()
    repo = await client.get_repo(repo_name)
    await repo.checkout()
    _tree = await repo.tree(prefix=prefix, depth=depth)

    if output == "json":
        print_json(_tree.model_dump_json())
    else:
        rich_console.print(_tree._as_rich_tree(name=repo_name))


@app.command(hidden=True)
@coro  # type: ignore
async def get_status(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    repo = await AsyncClient().get_repo_object(repo_name)
    if output == "json":
        print_json(data=repo.status.model_dump())
    else:
        print(repo.status.mode.value)


@app.command(hidden=True)
@coro  # type: ignore
async def set_status(
    repo_name: str = typer.Argument(..., help="Name of repository {ORG}/{REPO_NAME}"),
    mode: RepoOperationMode = typer.Argument(..., help="An option"),
    message: str = typer.Option(None, help="Optional message to bind to state"),
    output: ListOutputType = typer.Option("rich", help="Output formatting"),
):
    c = AsyncClient()
    await c._set_repo_status(repo_name, mode, message)
    repo = await c.get_repo_object(repo_name)
    if output == "json":
        print_json(data=repo.status.model_dump())
    else:
        print(repo.status.mode.value)
