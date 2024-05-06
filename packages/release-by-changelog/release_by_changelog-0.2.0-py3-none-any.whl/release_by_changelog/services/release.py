from __future__ import annotations

import contextlib
import functools
import http
import os
import pathlib
import re
import typing

import gitlab.v4
import gitlab.v4.objects
import typer

from release_by_changelog import logging
from release_by_changelog.typings_ import Version

TARGET_RELEASE: typing.Final[dict[bool, typing.Literal["tags", "releases"]]] = {
    True: "tags",
    False: "releases",
}

REGEX: typing.Final = re.compile(
    r"^## \[(?P<version>(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]"
    r"\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*"
    r"|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA"
    r"-Z-]+)*))?)\]"
)


class Release:
    project_id: str
    ref: str
    changelog_path: pathlib.Path
    host: str
    interact: bool
    token: str

    def __init__(
        self: typing.Self,
        project_id: str,
        ref: str,
        changelog_path: pathlib.Path,
        host: str,
        interact: bool,
        token: str,
    ) -> None:
        self.project_id = project_id
        self.ref = ref
        self.changelog_path = changelog_path
        self.host = host
        self.interact = interact
        self.token = token

    @functools.cached_property
    def tmp_changelog(self: typing.Self) -> pathlib.Path:
        """
        Save the remote changelog file to a temporary file.

        :raises NotImplementedError: If the OS is not supported.
        """
        if os.name == "posix":
            tmp_file = pathlib.Path(f"/tmp/{self.changelog_path.name}")
        elif os.name == "nt":
            temp_path = pathlib.Path(os.environ["Temp"])
            tmp_file = temp_path / self.changelog_path.name
        else:
            raise NotImplementedError(f"OS {os.name} not supported")
        tmp_file.write_bytes(self.remote_changelog.decode())
        return tmp_file

    @functools.cached_property
    def remote_changelog(
        self: typing.Self,
    ) -> gitlab.v4.objects.ProjectFile:
        try:
            changelog_file: gitlab.v4.objects.ProjectFile = self.project.files.get(
                file_path=str(self.changelog_path), ref=self.ref
            )
        except gitlab.GitlabGetError as e:
            if e.response_code == http.HTTPStatus.NOT_FOUND:
                logging.error(
                    f"[bold red]Changelog file {self.changelog_path} not found in the "
                    f"remote project files[/bold red]"
                )
                raise typer.Exit(code=1)
            raise e
        logging.success(
            f"[bold cyan]{self.changelog_path}[/bold cyan] found in the remote project "
            "files"
        )
        return changelog_file

    @functools.cached_property
    def local_changelog(self: typing.Self) -> pathlib.Path:
        logging.info(f"Look for local [bold cyan]{self.changelog_path}[/bold cyan]")
        if self.changelog_path.exists():
            logging.success(f"Found local [bold cyan]{self.changelog_path}[/bold cyan]")
            return self.changelog_path

        logging.warn(
            f"Local [bold cyan]{self.changelog_path}[/bold cyan] file not found, "
            "looking for file in the remote project files"
        )

        return self.tmp_changelog

    @staticmethod
    def extract_last_version(f: typing.TextIO) -> str:
        for lines in f:
            matches = REGEX.finditer(lines)
            try:
                match = next(matches)
            except StopIteration:
                continue
            return match.group("version")
        raise ValueError("No changelog entry found")

    @staticmethod
    def extract_description(f: typing.TextIO) -> str:
        body = []
        for lines in f:
            matches = REGEX.finditer(lines)
            with contextlib.suppress(StopIteration):
                next(matches)
                break

            body.append(lines)
        return "".join(body)

    @functools.cached_property
    def version(self: typing.Self) -> Version:
        """Extract the last changelog entry from the changelog file."""
        logging.info(f"Processing [bold cyan]{self.local_changelog}[/bold cyan]")
        with self.local_changelog.open() as f:
            version = self.extract_last_version(f)
            description = self.extract_description(f)
        logging.success(f"Found changelog entry: [bold cyan]{version}[/bold cyan]")
        return Version(name=version, description=description)

    @functools.cached_property
    def project(self: typing.Self) -> gitlab.v4.objects.Project:
        logging.info(
            f"Retrieving project [bold cyan]{self.project_id}[/bold cyan] from "
            f"[bold cyan]{self.host}[/bold cyan]"
        )
        url = f"https://{self.host}"
        gl = gitlab.Gitlab(url=url, oauth_token=self.token)
        try:
            project = gl.projects.get(self.project_id)
        except gitlab.GitlabAuthenticationError as e:
            if e.response_code == http.HTTPStatus.UNAUTHORIZED:
                logging.error(
                    logging.err_panel(
                        "Possible remediation:\n"
                        "\t- Check if the provided token is correct.\n"
                        "\t- Check if the provided token has the correct permissions "
                        "and scope, is not expired or revoked.",
                        title="Error: Unauthorized",
                    )
                )
                raise typer.Exit(code=1)
            raise e
        except gitlab.GitlabGetError as e:
            if e.response_code == http.HTTPStatus.NOT_FOUND:
                logging.error(
                    logging.err_panel(
                        "Possible remediation:\n"
                        "\t- Provide the project ID. To find the project ID, go to the "
                        "project page, click on the three vertical dot button on the "
                        "top right corner and press the 'Copy project ID: XXXX' "
                        "button.\n"
                        "\t- Provide the full path to the project. To find it, go to "
                        "the project page, check at the url and copy the path after the"
                        " host. If the following link doesn't point to your project, "
                        "you could have the namespace wrong: "
                        f"'https://{self.host}/{self.project_id}'\n"
                        "\t- Check if the host is correct. If you are using a "
                        "self-hosted GitLab, you need to provide the correct host. "
                        f"Current host: 'https://{self.host}', is that where your "
                        f"project is hosted?\n",
                        title="Error: Project not found.",
                    )
                )
                raise typer.Exit(code=1)
            raise e
        project_path = f"{project.namespace.get('full_path')}/{project.name}"
        logging.success(f"Project found: [bold cyan]{project_path}[bold cyan]")
        return project

    @functools.cached_property
    def project_path(self: typing.Self) -> str:
        return f"{self.project.namespace.get('full_path')}/{self.project.name}"

    def publish(self: typing.Self, tag_only: bool) -> None:
        logging.info(
            f"Creating release [bold cyan]{self.version.name}[/bold cyan] for "
            f"project [bold cyan]{self.project_path}[/bold cyan]"
        )
        data = {
            "tag_name": self.version.name,
            "ref": self.ref,
        }

        target_attr = TARGET_RELEASE[tag_only]
        target = getattr(self.project, target_attr)

        try:
            target.create(data)
        except gitlab.GitlabAuthenticationError as e:
            if e.response_code == http.HTTPStatus.UNAUTHORIZED:
                logging.error(
                    logging.err_panel(
                        "Possible remediation:\n"
                        "\t- Check if the provided token is correct.\n"
                        "\t- Check if the provided token has the correct permissions "
                        "and scope, is not expired or revoked.",
                        title="Error: Unauthorized",
                    )
                )
                raise typer.Exit(code=1)
            raise e
        except gitlab.GitlabCreateError as e:
            if e.response_code == http.HTTPStatus.CONFLICT:
                logging.error(
                    logging.err_panel(
                        f"It looks like the {target_attr} [bold cyan]"
                        f"{self.version.name}[/bold cyan] already exists.\n"
                        "Possible remediation: Bump the version in the changelog file.",
                        title=f"Error: {target_attr.capitalize()} already " f"exists",
                    )
                )
                raise typer.Exit(code=1)
            raise e
        logging.success(f"Release created: {self.version.name}")
