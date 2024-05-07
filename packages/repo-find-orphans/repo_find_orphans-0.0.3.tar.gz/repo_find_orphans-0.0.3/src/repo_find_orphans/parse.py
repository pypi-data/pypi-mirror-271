from pathlib import Path

import defusedxml.ElementTree as ET  # noqa: N817
from repo_find_orphans.types.project import Project


def parse_manifest(file_path: Path) -> list[Project]:
    def extract_projects(file_content: str) -> list[Project]:
        tree = ET.fromstring(file_content, forbid_dtd=True, forbid_entities=True, forbid_external=True)
        projects: list[Project] = []
        for project_elem in tree.findall("project"):
            name = project_elem.get("name") or ""
            path = project_elem.get("path") or ""
            revision = project_elem.get("revision")
            remote = project_elem.get("remote")
            projects.append(Project(name, path, revision, remote))
        return projects

    with file_path.open() as f:
        return extract_projects(f.read())
