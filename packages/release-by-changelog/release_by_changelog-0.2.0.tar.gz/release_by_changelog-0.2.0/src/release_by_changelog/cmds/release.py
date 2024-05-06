from __future__ import annotations

import pathlib
import typing

import typer

import release_by_changelog.services.release
from release_by_changelog.app import app
from release_by_changelog.cmds._release import get_token


@app.command()
def release(
    project: str = typer.Argument(help="Path or id on host.", envvar="CI_PROJECT_ID"),
    ref: str = typer.Argument(
        help="Can be a branch, tag, or commit SHA.",
        envvar="CI_COMMIT_SHA",
    ),
    changelog_path: typing.Annotated[
        pathlib.Path,
        typer.Option(help="Path to the changelog file."),
    ] = pathlib.Path("CHANGELOG.md"),
    host: typing.Annotated[
        str,
        typer.Option(
            help="URL of the GitLab instance.",
            envvar="CI_SERVER_HOST",
        ),
    ] = "gitlab.com",
    token: str = typer.Option(
        None,
        help="[red]Required[/red] for [yellow]user-based[/yellow] authentication.",
        envvar="PRIVATE_TOKEN",
    ),
    ci_job_token: str = typer.Option(
        None,
        help="[red]Required[/red] for [yellow]CI-based[/yellow] authentication.",
        envvar="CI_JOB_TOKEN",
    ),
    interact: bool = typer.Option(
        True,
        help="CLI ask for confirmation before creating the release. "
        "No interaction means automatic confirmation.",
    ),
    tag_only: bool = typer.Option(
        False,
        help="Only tag the commit with the changelog version.",
        is_flag=True,
    ),
) -> None:
    token = get_token(ci_job_token, token)
    release_ = release_by_changelog.services.release.Release(
        project_id=project,
        ref=ref,
        changelog_path=changelog_path,
        host=host,
        interact=interact,
        token=token,
    )
    release_.publish(tag_only)
