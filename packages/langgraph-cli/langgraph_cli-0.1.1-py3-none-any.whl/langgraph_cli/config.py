import json
import os
import pathlib
from typing import TypedDict, Union


class Config(TypedDict):
    dependencies: list[str]
    graphs: dict[str, str]
    env: Union[dict[str, str], str]


def config_to_compose(config_path: pathlib.Path, config: Config):
    pypi_deps = [dep for dep in config["dependencies"] if not dep.startswith(".")]
    local_pkgs = []
    faux_pkgs = {}
    locals_set = set()

    for local_dep in config["dependencies"]:
        if local_dep.startswith("."):
            resolved = config_path.parent / local_dep

            # validate local dependency
            if not resolved.exists():
                raise FileNotFoundError(f"Could not find local dependency: {resolved}")
            elif not resolved.is_dir():
                raise NotADirectoryError(
                    f"Local dependency must be a directory: {resolved}"
                )
            elif resolved.name in locals_set:
                raise ValueError(f"Duplicate local dependency: {resolved}")
            else:
                locals_set.add(resolved.name)

            # if it's installable, add it to local_pkgs
            # otherwise, add it to faux_pkgs, and create a pyproject.toml
            files = os.listdir(resolved)
            if "pyproject.toml" in files:
                local_pkgs.append(local_dep)
            elif "setup.py" in files:
                local_pkgs.append(local_dep)
            else:
                faux_pkgs[resolved.name] = local_dep

    for _, import_str in config["graphs"].items():
        module_str, _, attrs_str = import_str.partition(":")
        if not module_str or not attrs_str:
            message = (
                'Import string "{import_str}" must be in format "<module>:<attribute>".'
            )
            raise ValueError(message.format(import_str=import_str))

    faux_pkgs_str = "\n\n".join(
        f"ADD {path} /tmp/{name}/{name}\n                RUN touch /tmp/{name}/pyproject.toml"
        for name, path in faux_pkgs.items()
    )
    local_pkgs_str = f"ADD {' '.join(local_pkgs)} /tmp/" if local_pkgs else ""
    env_vars_str = (
        "\n".join(f"            {k}: {v}" for k, v in config["env"].items())
        if isinstance(config["env"], dict)
        else ""
    )
    env_file_str = (
        f"env_file: {config['env']}" if isinstance(config["env"], str) else ""
    )

    return f"""
            LANGSERVE_GRAPHS: '{json.dumps(config["graphs"])}'
            {env_vars_str}
        {env_file_str}
        pull_policy: build
        build:
            dockerfile_inline: |
                FROM langchain/langserve

                {local_pkgs_str}

                {faux_pkgs_str}

                RUN pip install {' '.join(pypi_deps)} /tmp/*
"""
