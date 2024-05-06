import collections.abc

import click.testing
import pytest


@pytest.mark.usefixtures("successful_gitlab_interaction_project")
def test_release_local_changelog(
    app: collections.abc.Callable[[list[str]], click.testing.Result],
) -> None:
    local_changelog = "tests/CHANGELOG.md"
    result = app(
        [
            "--changelog-path",
            local_changelog,
            "--token",
            "TOKEN",
            "--host",
            "HOST",
            "3",
            "main",
        ]
    )
    assert result.exit_code == 0, result.stdout
    assert f"Look for local {local_changelog}" in result.output
    assert f"Found local {local_changelog}" in result.output
    assert f"Processing {local_changelog}" in result.output
    assert "Found changelog entry: 1.0.0" in result.output
    assert "Retrieving project 3 from HOST" in result.output
    assert "Project found: diaspora/Diaspora" in result.output
    assert (
        "Creating release 1.0.0 for project diaspora/Diaspora Project Site"
        in result.output
    )
    assert "Release created: 1.0.0" in result.output


@pytest.mark.usefixtures("successful_gitlab_interaction_project_file")
def test_release_remote_changelog(
    app: collections.abc.Callable[[list[str]], click.testing.Result],
) -> None:
    result = app(
        ["--changelog-path", "FILE", "--token", "TOKEN", "--host", "HOST", "3", "main"]
    )
    assert result.exit_code == 0, result.stdout
    assert "Look for local FILE" in result.output
    assert (
        "Local FILE file not found, looking for file in the remote project files"
        in result.output
    )
    assert "Retrieving project 3 from HOST" in result.output
    assert "Project found: diaspora/Diaspora" in result.output
    assert "FILE found in the remote project files" in result.output
    assert "Found changelog entry: 1.0.0" in result.output
    assert (
        "Creating release 1.0.0 for project diaspora/Diaspora Project Site"
        in result.output
    )
    assert "Release created: 1.0.0" in result.output


@pytest.mark.usefixtures("project_not_found_gitlab_interaction")
def test_release_read_project_not_found(
    app: collections.abc.Callable[[list[str]], click.testing.Result],
) -> None:
    result = app(
        ["--changelog-path", "FILE", "--token", "TOKEN", "--host", "HOST", "3", "main"]
    )
    assert result.exit_code == 1, result.stdout
    assert "Look for local FILE" in result.output
    assert (
        "Local FILE file not found, looking for file in the remote project files"
        in result.output
    )
    assert "Retrieving project 3 from HOST" in result.output
    assert "Error: Project not found" in result.output
    assert "release_by_changelog --help" in result.output


@pytest.mark.usefixtures("unauthorized_gitlab_interaction")
def test_release_read_project_unauthorized(
    app: collections.abc.Callable[[list[str]], click.testing.Result],
) -> None:
    result = app(
        ["--changelog-path", "FILE", "--token", "TOKEN", "--host", "HOST", "3", "main"]
    )
    assert result.exit_code == 1, result.stdout
    assert "Look for local FILE" in result.output
    assert (
        "Local FILE file not found, looking for file in the remote project files"
        in result.output
    )
    assert "Retrieving project 3 from HOST" in result.output
    assert "Error: Unauthorized" in result.output
    assert "release_by_changelog --help" in result.output


@pytest.mark.usefixtures("unauthorized_publish_gitlab_interaction")
def test_release_read_project_unauthorized_publish(
    app: collections.abc.Callable[[list[str]], click.testing.Result],
) -> None:
    result = app(
        ["--changelog-path", "FILE", "--token", "TOKEN", "--host", "HOST", "3", "main"]
    )
    print(result.stdout)
    assert result.exit_code == 1, result.stdout
    assert "Look for local FILE" in result.output
    assert (
        "Local FILE file not found, looking for file in the remote project files"
        in result.output
    )
    assert "Retrieving project 3 from HOST" in result.output
    assert "Project found: diaspora/Diaspora Project Site" in result.output
    assert "FILE found in the remote project files" in result.output
    assert "Processing /tmp/FILE" in result.output
    assert "Found changelog entry: 1.0.0" in result.output
    assert (
        "Creating release 1.0.0 for project diaspora/Diaspora Project Site"
        in result.output
    )
    assert "Error: Unauthorized" in result.output
    assert "release_by_changelog --help" in result.output


@pytest.mark.usefixtures("successful_gitlab_interaction_project_file")
def test_tag(
    app: collections.abc.Callable[[list[str]], click.testing.Result],
) -> None:
    result = app(
        [
            "--changelog-path",
            "FILE",
            "--token",
            "TOKEN",
            "--host",
            "HOST",
            "--tag-only",
            "3",
            "main",
        ]
    )
    assert result.exit_code == 0, result.stdout
    assert "Look for local FILE" in result.output
    assert (
        "Local FILE file not found, looking for file in the remote project files"
        in result.output
    )
    assert "Retrieving project 3 from HOST" in result.output
    assert "Project found: diaspora/Diaspora Project Site" in result.output
    assert "FILE found in the remote project files" in result.output
    assert "Found changelog entry: 1.0.0" in result.output
    assert (
        "Creating release 1.0.0 for project diaspora/Diaspora Project Site"
        in result.output
    )
    assert "Release created: 1.0.0" in result.output
