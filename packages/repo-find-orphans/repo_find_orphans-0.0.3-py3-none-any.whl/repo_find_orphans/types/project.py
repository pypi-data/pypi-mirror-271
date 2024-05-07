from dataclasses import dataclass


@dataclass
class Project:
    name: str
    path: str
    revision: str | None = None
    remote: str | None = None

    def __repr__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        return f"Project(name={self.name}, path={self.path}, revision={self.revision}, remote={self.remote})"
