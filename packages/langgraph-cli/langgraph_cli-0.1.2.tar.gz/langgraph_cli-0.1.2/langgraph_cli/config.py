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
    local_pkgs: dict[pathlib.Path, str] = {}
    faux_pkgs: dict[pathlib.Path, str] = {}
    pkg_names = set()

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
            elif resolved.name in pkg_names:
                raise ValueError(f"Duplicate local dependency: {resolved}")
            else:
                pkg_names.add(resolved.name)

            # if it's installable, add it to local_pkgs
            # otherwise, add it to faux_pkgs, and create a pyproject.toml
            files = os.listdir(resolved)
            if "pyproject.toml" in files:
                local_pkgs[resolved] = local_dep
            elif "setup.py" in files:
                local_pkgs[resolved] = local_dep
            else:
                faux_pkgs[resolved] = local_dep

    for graph_id, import_str in config["graphs"].items():
        module_str, _, attr_str = import_str.partition(":")
        if not module_str or not attr_str:
            message = (
                'Import string "{import_str}" must be in format "<module>:<attribute>".'
            )
            raise ValueError(message.format(import_str=import_str))
        if module_str.startswith("."):
            resolved = config_path.parent / module_str
            if not resolved.exists():
                raise FileNotFoundError(f"Could not find local module: {resolved}")
            elif not resolved.is_file():
                raise IsADirectoryError(f"Local module must be a file: {resolved}")
            else:
                for local_pkg in local_pkgs:
                    if resolved.is_relative_to(local_pkg):
                        resolved = resolved.relative_to(local_pkg)
                        break
                else:
                    for faux_pkg in faux_pkgs:
                        if resolved.is_relative_to(faux_pkg):
                            resolved = resolved.relative_to(faux_pkg.parent)
                            break
                    else:
                        raise ValueError(
                            f"Module '{import_str}' not found in 'dependencies' list"
                            "Add its containing package to 'dependencies' list."
                        )
            # rewrite module_str to be a python import path
            module_str = f"{'.'.join(resolved.parts[:-1])}"
            if resolved.stem == "__init__":
                pass
            else:
                module_str = f"{module_str}.{resolved.stem}"
            # update the config
            config["graphs"][graph_id] = f"{module_str}:{attr_str}"

    faux_pkgs_str = "\n\n".join(
        f"ADD {relpath} /tmp/{fullpath.name}/{fullpath.name}\n                RUN touch /tmp/{fullpath.name}/pyproject.toml"
        for fullpath, relpath in faux_pkgs.items()
    )
    local_pkgs_str = f"ADD {' '.join(local_pkgs.values())} /tmp/" if local_pkgs else ""
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
