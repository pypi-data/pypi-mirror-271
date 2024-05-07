from pathlib import Path

from repo_find_orphans.types.project import Project
from rich.console import Console
from rich.progress import track

ignored_files = {
    ".DS_Store",
}


def scan_projects(path: Path, projects: list[Project]) -> set[Path]:
    project_paths = {Path(project.path) for project in projects}
    dirs: set[Path] = set()

    rglob = list(Path(path).rglob("*"))
    if Console().is_terminal:
        rglob = track(rglob, description="Scan: ")

    for gpath in rglob:
        # Filter out directories that are part of the project paths
        if gpath.is_dir():
            continue
        if gpath.name in ignored_files:
            continue

        clean_path = gpath.relative_to(Path(path))

        if any(str(clean_path).startswith(str(proj_path)) for proj_path in project_paths):
            continue
        if any(str(clean_path).startswith(str(proj_path)) for proj_path in dirs):
            continue

        dirs.add(clean_path.parent)

    return dirs
