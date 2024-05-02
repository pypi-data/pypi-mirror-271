import os
from dataclasses import dataclass, field
from SCons.Environment import Environment


@dataclass
class Build:
    name: str

    files: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)

    packages: dict[str, list[str]] = field(default_factory=dict)

    output: str = "dist"
    shared: bool = False

    rename: str | None = None

    def __repr__(self) -> str:
        return self.name

    @property
    def target(self) -> str:
        return os.path.join(self.output, self.rename if self.rename else self.name)

    @property
    def merge(self) -> dict[str, list[str]]:
        packages = self.packages.copy()
        packages["CXXFLAGS"] = packages.get("CXXFLAGS", []) + self.flags
        return packages

    def path(self, file: str) -> str:
        root = os.path.splitext(os.path.normpath(file))[0]
        return f"{root.replace('.', '-')}-[{self.name}]"

    def nodes(self, env: Environment) -> list[str]:
        return [env.Object(self.path(file), file, **self.merge) for file in self.files]

    def register(self, env: Environment) -> None:
        if self.shared:
            outputs = env.Library(self.target, self.nodes(env), **self.merge)
            env.Alias(self.name, outputs[0])
        else:
            env.Program(self.target, self.nodes(env), **self.merge)
            env.Alias(self.name, self.target)
