from __future__ import annotations

import typer

from release_by_changelog import logging


def get_token(ci_job_token: str | None, token: str | None) -> str:
    """
    Get the token from the environment variables or the CLI.

    :raises typer.Exit: If no token is provided.
    """
    match (token, ci_job_token):
        case (str(value), _) | (_, str(value)):
            return value
        case _:
            logging.error(
                logging.err_panel(
                    "You need to provide a PRIVATE_TOKEN or a CI_JOB_TOKEN",
                    title="Error: Missing token",
                )
            )
            raise typer.Exit(code=1)
