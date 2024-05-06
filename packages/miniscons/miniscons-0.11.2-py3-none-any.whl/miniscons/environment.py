import os
import psutil
from .constants import SCONS_FLAGS
from emoji import emojize
from SCons.Environment import Environment
from SCons.Script import SConscript


def conan(
    defines: list[str] | None = None,
    source: str = "SConscript_conandeps",
) -> tuple[Environment, list[str]]:
    if defines is None:
        defines = []

    env = Environment(
        num_jobs=psutil.cpu_count(),
        ENV={"PATH": os.getenv("PATH", "")},
        CXXCOMSTR=emojize(":wrench: Compiling $TARGET"),
        LINKCOMSTR=emojize(":link: Linking $TARGET"),
    )

    conandeps = SConscript(source)["conandeps"]
    conandeps["CPPDEFINES"] += defines

    env.MergeFlags(conandeps)
    return env


def packages(
    names: list[str],
    libs: list[str] | None = None,
    explicit: bool = False,
    source: str = "SConscript_conandeps",
) -> dict[str, list[str]]:
    if libs is None:
        libs = names.copy()

    if not explicit:
        names.append("conandeps")

    reduced = {"LIBS": libs}

    for name, package in SConscript(source).items():
        if name in names:
            for flag in SCONS_FLAGS:
                reduced[flag] = reduced.get(flag, []) + package.get(flag, [])

    return reduced
