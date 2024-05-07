import functools

import rich.panel
import rich.table

_console = rich.console.Console()

success = functools.partial(_console.print, style="bold green")
info = functools.partial(_console.print)
warn = functools.partial(_console.print, style="yellow")

_err_console = rich.console.Console(stderr=True)
err_panel = functools.partial(
    rich.panel.Panel,
    title_align="left",
    subtitle="release_by_changelog --help",
    subtitle_align="left",
    expand=False,
    border_style="red",
)
error = functools.partial(_err_console.print, style="bold red")
