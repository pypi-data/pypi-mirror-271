# Release by Changelog

[![Pipeline](https://lab.frogg.it/swepy/release-by-changelog/badges/main/pipeline.svg)](https://lab.frogg.it/swepy/release-by-changelog/-/pipelines?ref=main)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


Release a new version of a software based on CHANGELOG.md file.

Detect the latest version in the CHANGELOG.md file and create a new release in the 
repository. 

Release by Changelog rely on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) 
format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html), following those 
two norms is required.

## Installation

```bash
pip install --upgrade pip
pip install release-by-changelog
```

## Usage

In a Gitlab CI pipeline, you can use the following command to release a new version of
your software based on the CHANGELOG.md file.

```bash
release-by-changelog
```

It's recommended to add a `rules` section to run this command only on the default 
branch.

Here is an example of a `.gitlab-ci.yml` file using `release-by-changelog`:

```yaml
release:
    stage: deploy
    script:
        - pip install release-by-changelog 
        - release-by-changelog
    rules:
        -   if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

`release-by-changelog` will read the CHANGELOG.md file and create a new tag based on the
latest version found in the file. The release will be pushed to the repository. 

`release-by-changelog` rely on the following predefined CI/CD variables to authenticate 
with the GitLab API:

- `CI_PROJECT_ID`: Used to identify the project,
- `CI_COMMIT_SHA`: Used to identify the reference,
- `CI_JOB_TOKEN`: Used to authenticate with the GitLab API.
- `CI_SERVER_HOST`: Used to identify the GitLab host.

### Local usage

You can also use this command locally to release a new version of your software.

```bash
release-by-changelog --token <token> <project> <ref>
```

* project: Path or id on host. [required]
* ref: Can be a branch, tag, or commit SHA. [required]

The token is required to authenticate with the GitLab API.
You can authenticate with the GitLab API in several ways:

- [OAuth 2.0 tokens](https://docs.gitlab.com/ee/api/rest/#oauth-20-tokens)
- [Personal access tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
- [Project access tokens](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html)
- [Group access tokens](https://docs.gitlab.com/ee/user/group/settings/group_access_tokens.html)

### Using environment variables

You can also use environment variables to avoid passing the token each time. A token
passed as an argument will always take precedence over the environment variable.

```bash
export PRIVATE_TOKEN=<token>
release-by-changelog <project> <ref>
```
