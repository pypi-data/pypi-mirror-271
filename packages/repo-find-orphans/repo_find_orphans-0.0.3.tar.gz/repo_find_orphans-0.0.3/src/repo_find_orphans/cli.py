from pathlib import Path
from typing import Annotated

import typer
from repo_find_orphans.parse import parse_manifest
from repo_find_orphans.scan import scan_projects

app = typer.Typer()


@app.command()
def scan_projects_cli(
    manifest_file: Annotated[Path, typer.Argument(help="Manifest file", exists=True, file_okay=True, dir_okay=False)],
    project_dir: Annotated[Path, typer.Argument(help="Project directory", exists=True, file_okay=False, dir_okay=True)],
):
    projects = parse_manifest(manifest_file)
    new_dirs = scan_projects(project_dir, projects)

    for orphan in new_dirs:
        print(orphan)  # noqa: T201


app()
