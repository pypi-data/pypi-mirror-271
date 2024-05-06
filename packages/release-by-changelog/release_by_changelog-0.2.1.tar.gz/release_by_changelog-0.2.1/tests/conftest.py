import base64
import collections.abc
import functools
import hashlib
import http
import pathlib

import click.testing
import gitlab.exceptions
import pytest
import pytest_mock
import typer.testing
from release_by_changelog.app import app as rbc_app


@pytest.fixture
def runner() -> typer.testing.CliRunner:
    return typer.testing.CliRunner()


@pytest.fixture
def app(
    runner: typer.testing.CliRunner,
) -> collections.abc.Callable[[list[str]], click.testing.Result]:
    return functools.partial(runner.invoke, rbc_app)


# https://docs.gitlab.com/ee/api/projects.html#get-single-project
project_data = {
    "id": 3,
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    "description_html": '<p data-sourcepos="1:1-1:56" dir="auto">Lorem ipsum dolor sit '
    "amet, consectetur adipiscing elit.</p>",
    "default_branch": "main",
    "visibility": "private",
    "ssh_url_to_repo": "git@example.com:diaspora/diaspora-project-site.git",
    "http_url_to_repo": "http://example.com/diaspora/diaspora-project-site.git",
    "web_url": "http://example.com/diaspora/diaspora-project-site",
    "readme_url": "http://example.com/diaspora/diaspora-project-site/blob/main"
    "/README.md",
    "tag_list": ["example", "disapora project"],
    "topics": ["example", "disapora project"],
    "owner": {"id": 3, "name": "Diaspora", "created_at": "2013-09-30T13:46:02Z"},
    "name": "Diaspora Project Site",
    "name_with_namespace": "Diaspora / Diaspora Project Site",
    "path": "diaspora-project-site",
    "path_with_namespace": "diaspora/diaspora-project-site",
    "issues_enabled": True,
    "open_issues_count": 1,
    "merge_requests_enabled": True,
    "jobs_enabled": True,
    "wiki_enabled": True,
    "snippets_enabled": False,
    "can_create_merge_request_in": True,
    "resolve_outdated_diff_discussions": False,
    "container_registry_enabled": False,
    "container_registry_access_level": "disabled",
    "security_and_compliance_access_level": "disabled",
    "container_expiration_policy": {
        "cadence": "7d",
        "enabled": False,
        "keep_n": None,
        "older_than": None,
        "name_regex": None,
        "name_regex_delete": None,
        "name_regex_keep": None,
        "next_run_at": "2020-01-07T21:42:58.658Z",
    },
    "created_at": "2013-09-30T13:46:02Z",
    "updated_at": "2013-09-30T13:46:02Z",
    "last_activity_at": "2013-09-30T13:46:02Z",
    "creator_id": 3,
    "namespace": {
        "id": 3,
        "name": "Diaspora",
        "path": "diaspora",
        "kind": "group",
        "full_path": "diaspora",
        "avatar_url": "http://localhost:3000/uploads/group/avatar/3/foo.jpg",
        "web_url": "http://localhost:3000/groups/diaspora",
    },
    "import_url": None,
    "import_type": None,
    "import_status": "none",
    "import_error": None,
    "permissions": {
        "project_access": {"access_level": 10, "notification_level": 3},
        "group_access": {"access_level": 50, "notification_level": 3},
    },
    "archived": False,
    "avatar_url": "http://example.com/uploads/project/avatar/3/uploads/avatar.png",
    "license_url": "http://example.com/diaspora/diaspora-client/blob/main/LICENSE",
    "license": {
        "key": "lgpl-3.0",
        "name": "GNU Lesser General Public License v3.0",
        "nickname": "GNU LGPLv3",
        "html_url": "http://choosealicense.com/licenses/lgpl-3.0/",
        "source_url": "http://www.gnu.org/licenses/lgpl-3.0.txt",
    },
    "shared_runners_enabled": True,
    "group_runners_enabled": True,
    "forks_count": 0,
    "star_count": 0,
    "runners_token": "b8bc4a7a29eb76ea83cf79e4908c2b",
    "ci_default_git_depth": 50,
    "ci_forward_deployment_enabled": True,
    "ci_forward_deployment_rollback_allowed": True,
    "ci_allow_fork_pipelines_to_run_in_parent_project": True,
    "ci_separated_caches": True,
    "ci_restrict_pipeline_cancellation_role": "developer",
    "public_jobs": True,
    "shared_with_groups": [
        {
            "group_id": 4,
            "group_name": "Twitter",
            "group_full_path": "twitter",
            "group_access_level": 30,
        },
        {
            "group_id": 3,
            "group_name": "Gitlab Org",
            "group_full_path": "gitlab-org",
            "group_access_level": 10,
        },
    ],
    "repository_storage": "default",
    "only_allow_merge_if_pipeline_succeeds": False,
    "allow_merge_on_skipped_pipeline": False,
    "restrict_user_defined_variables": False,
    "only_allow_merge_if_all_discussions_are_resolved": False,
    "remove_source_branch_after_merge": False,
    "printing_merge_requests_link_enabled": True,
    "request_access_enabled": False,
    "merge_method": "merge",
    "squash_option": "default_on",
    "auto_devops_enabled": True,
    "auto_devops_deploy_strategy": "continuous",
    "approvals_before_merge": 0,
    "mirror": False,
    "mirror_user_id": 45,
    "mirror_trigger_builds": False,
    "only_mirror_protected_branches": False,
    "mirror_overwrites_diverged_branches": False,
    "external_authorization_classification_label": None,
    "packages_enabled": True,
    "service_desk_enabled": False,
    "service_desk_address": None,
    "autoclose_referenced_issues": True,
    "suggestion_commit_message": None,
    "enforce_auth_checks_on_uploads": True,
    "merge_commit_template": None,
    "squash_commit_template": None,
    "issue_branch_template": "gitlab/%{id}-%{title}",
    "marked_for_deletion_at": "2020-04-03",
    "marked_for_deletion_on": "2020-04-03",
    "compliance_frameworks": ["sox"],
    "warn_about_potentially_unwanted_characters": True,
    "statistics": {
        "commit_count": 37,
        "storage_size": 1038090,
        "repository_size": 1038090,
        "wiki_size": 0,
        "lfs_objects_size": 0,
        "job_artifacts_size": 0,
        "pipeline_artifacts_size": 0,
        "packages_size": 0,
        "snippets_size": 0,
        "uploads_size": 0,
    },
    "container_registry_image_prefix": "registry.example.com/diaspora/diaspora-client",
    "_links": {
        "self": "http://example.com/api/v4/projects",
        "issues": "http://example.com/api/v4/projects/1/issues",
        "merge_requests": "http://example.com/api/v4/projects/1/merge_requests",
        "repo_branches": "http://example.com/api/v4/projects/1/repository_branches",
        "labels": "http://example.com/api/v4/projects/1/labels",
        "events": "http://example.com/api/v4/projects/1/events",
        "members": "http://example.com/api/v4/projects/1/members",
        "cluster_agents": "http://example.com/api/v4/projects/1/cluster_agents",
    },
}

changelog_test_file = pathlib.Path("tests/CHANGELOG.md")

# https://docs.gitlab.com/ee/api/releases/#create-a-release with some modifications
file_data = {
    "file_name": changelog_test_file.name,  # Alteration to match expected name
    "file_path": str(changelog_test_file),  # Alteration to match expected path
    "size": changelog_test_file.stat().st_size,
    "encoding": "base64",
    # Alteration to match expected content
    "content": base64.b64encode(changelog_test_file.read_bytes()),
    # Alteration to match expected sha256
    "content_sha256": hashlib.sha256(changelog_test_file.read_bytes()).hexdigest(),
    "ref": "main",
    "blob_id": "79f7bbd25901e8334750839545a9bd021f0e4c83",
    "commit_id": "d5a3ff139356ce33e37e73add446f16869741b50",
    "last_commit_id": "570e7b2abdd848b95f2f578043fc23bd6f6fd24d",
    "execute_filemode": False,
}

# https://docs.gitlab.com/ee/api/releases/#create-a-release
release = {
    "tag_name": "v0.3",
    "description": "Super nice release",
    "name": "New release",
    "created_at": "2019-01-03T02:22:45.118Z",
    "released_at": "2019-01-03T02:22:45.118Z",
    "author": {
        "id": 1,
        "name": "Administrator",
        "username": "root",
        "state": "active",
        "avatar_url": "https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61"
        "?s=80\u0026d=identicon",
        "web_url": "https://gitlab.example.com/root",
    },
    "commit": {
        "id": "079e90101242458910cccd35eab0e211dfc359c0",
        "short_id": "079e9010",
        "title": "Update README.md",
        "created_at": "2019-01-03T01:55:38.000Z",
        "parent_ids": ["f8d3d94cbd347e924aa7b715845e439d00e80ca4"],
        "message": "Update README.md",
        "author_name": "Administrator",
        "author_email": "admin@example.com",
        "authored_date": "2019-01-03T01:55:38.000Z",
        "committer_name": "Administrator",
        "committer_email": "admin@example.com",
        "committed_date": "2019-01-03T01:55:38.000Z",
    },
    "milestones": [
        {
            "id": 51,
            "iid": 1,
            "project_id": 24,
            "title": "v1.0-rc",
            "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
            "state": "closed",
            "created_at": "2019-07-12T19:45:44.256Z",
            "updated_at": "2019-07-12T19:45:44.256Z",
            "due_date": "2019-08-16",
            "start_date": "2019-07-30",
            "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/1",
            "issue_stats": {"total": 99, "closed": 76},
        },
        {
            "id": 52,
            "iid": 2,
            "project_id": 24,
            "title": "v1.0",
            "description": "Voluptate fugiat possimus quis quod aliquam expedita.",
            "state": "closed",
            "created_at": "2019-07-16T14:00:12.256Z",
            "updated_at": "2019-07-16T14:00:12.256Z",
            "due_date": "2019-08-16",
            "start_date": "2019-07-30",
            "web_url": "https://gitlab.example.com/root/awesome-app/-/milestones/2",
            "issue_stats": {"total": 24, "closed": 21},
        },
    ],
    "commit_path": "/root/awesome-app/commit/588440f66559714280628a4f9799f0c4eb880a4a",
    "tag_path": "/root/awesome-app/-/tags/v0.11.1",
    "evidence_sha": "760d6cdfb0879c3ffedec13af470e0f71cf52c6cde4d",
    "assets": {
        "count": 5,
        "sources": [
            {
                "format": "zip",
                "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3"
                "/awesome-app-v0.3.zip",
            },
            {
                "format": "tar.gz",
                "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3"
                "/awesome-app-v0.3.tar.gz",
            },
            {
                "format": "tar.bz2",
                "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3"
                "/awesome-app-v0.3.tar.bz2",
            },
            {
                "format": "tar",
                "url": "https://gitlab.example.com/root/awesome-app/-/archive/v0.3"
                "/awesome-app-v0.3.tar",
            },
        ],
        "links": [
            {
                "id": 3,
                "name": "hoge",
                "url": "https://gitlab.example.com/root/awesome-app/-/tags/v0.11.1"
                "/binaries/linux-amd64",
                "link_type": "other",
            }
        ],
        "evidence_file_path": "https://gitlab.example.com/root/awesome-app/-/releases"
        "/v0.3/evidence.json",
    },
}


def fake_get_project() -> collections.abc.Callable:
    """Replace Gitlab.http_get (or other) method(s)."""

    def response_function(*_, **__) -> dict:
        return project_data

    return response_function


def fake_get_project_file() -> collections.abc.Callable:
    """Replace Gitlab.http_get (or other) method(s)."""
    responses = iter(
        [project_data, file_data]
    )  # A list of responses to return on each call

    def response_function(*_, **__) -> dict:
        return next(responses)

    return response_function


def fake_post() -> collections.abc.Callable:
    """Replace Gitlab.http_post (or other) method(s)."""
    responses = iter([release])  # A list of responses to return on each call

    def response_function(*_, **__) -> dict:
        return next(responses)

    return response_function


@pytest.fixture
def successful_gitlab_interaction_project(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch("gitlab.Gitlab.http_get", side_effect=fake_get_project())
    mocker.patch("gitlab.Gitlab.http_post", side_effect=fake_post())


@pytest.fixture
def successful_gitlab_interaction_project_file(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch("gitlab.Gitlab.http_get", side_effect=fake_get_project_file())
    mocker.patch("gitlab.Gitlab.http_post", side_effect=fake_post())


@pytest.fixture
def project_not_found_gitlab_interaction(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch(
        "gitlab.Gitlab.http_get",
        side_effect=gitlab.exceptions.GitlabHttpError(
            response_code=http.HTTPStatus.NOT_FOUND,
            error_message="404 Project Not Found",
            response_body=b'{"message":"404 Project Not Found"}',
        ),
    )


@pytest.fixture
def unauthorized_gitlab_interaction(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch(
        "gitlab.Gitlab.http_get",
        side_effect=gitlab.exceptions.GitlabAuthenticationError(
            response_code=http.HTTPStatus.UNAUTHORIZED,
            error_message="401 Unauthorized",
            response_body=b'{"message":"401 Unauthorized"}',
        ),
    )


@pytest.fixture
def unauthorized_publish_gitlab_interaction(mocker: pytest_mock.MockFixture) -> None:
    mocker.patch("gitlab.Gitlab.http_get", side_effect=fake_get_project_file())
    mocker.patch(
        "gitlab.Gitlab.http_post",
        side_effect=gitlab.exceptions.GitlabAuthenticationError(
            response_code=http.HTTPStatus.UNAUTHORIZED,
            error_message="401 Unauthorized",
            response_body=b'{"message":"401 Unauthorized"}',
        ),
    )
