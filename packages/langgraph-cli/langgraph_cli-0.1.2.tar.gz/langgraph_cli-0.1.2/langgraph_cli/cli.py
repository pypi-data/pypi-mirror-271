import asyncio
import json
import os
import pathlib
import shutil
import signal
from datetime import datetime, timezone
from typing import Coroutine, Optional

import click

import langgraph_cli.config
import langgraph_cli.docker


async def exec(cmd: str, *args: str, input: str = None, wait: float = None):
    if wait:
        await asyncio.sleep(wait)
    try:
        proc = await asyncio.create_subprocess_exec(
            cmd, *args, stdin=asyncio.subprocess.PIPE if input else None
        )
        await proc.communicate(input.encode() if input else None)
        if (
            proc.returncode != 0  # success
            and proc.returncode != 130  # user interrupt
        ):
            raise click.exceptions.Exit(proc.returncode)
    finally:
        try:
            if proc.returncode is None:
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGINT)
                except (ProcessLookupError, KeyboardInterrupt):
                    pass
        except UnboundLocalError:
            pass


PLACEHOLDER_NOW = object()


async def exec_loop(cmd: str, *args: str, input: str = None):
    now = datetime.now(timezone.utc).isoformat()
    while True:
        try:
            await exec(
                cmd, *(now if a is PLACEHOLDER_NOW else a for a in args), input=input
            )
            now = datetime.now(timezone.utc).isoformat()
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            pass


async def gather(*coros: Coroutine):
    tasks = [asyncio.create_task(coro) for coro in coros]
    exceptions = []
    while tasks:
        done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for t in tasks:
            t.cancel()
        for d in done:
            if exc := d.exception():
                exceptions.append(exc)


OPT_O = click.option(
    "--docker-compose",
    "-d",
    help="Advanced: Path to docker-compose.yml file with additional services to launch",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
OPT_C = click.option(
    "--config",
    "-c",
    help="""Path to configuration file declaring dependencies, graphs and environment variables.
    
    \b
    Example:
    {
        "dependencies": [
            "langchain_openai",
            "./your_package"
        ],
        "graphs": {
            "my_graph_id": "./your_package/your_file.py:variable"
        },
        "env": "./.env"
    }

    Defaults to looking for langgraph.json in the current directory.""",
    default="langgraph.json",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
OPT_PORT = click.option(
    "--port", "-p", type=int, default=8123, show_default=True, help="Port to expose"
)


@click.group()
def cli():
    pass


@click.option(
    "--recreate/--no-recreate",
    default=False,
    show_default=True,
    help="Clear previous data",
)
@click.option(
    "--pull/--no-pull", default=True, show_default=True, help="Pull latest images"
)
@OPT_PORT
@OPT_O
@OPT_C
@cli.command(help="Start langgraph API server")
def up(
    config: pathlib.Path,
    docker_compose: Optional[pathlib.Path],
    port: int,
    recreate: bool,
    pull: bool,
):
    with asyncio.Runner() as runner:
        # check docker available
        try:
            runner.run(exec("docker", "--version"))
            runner.run(exec("docker", "compose", "version"))
        except click.exceptions.Exit:
            click.echo("Docker not installed or not running")
            return
        # pull latest images
        if pull:
            runner.run(exec("docker", "pull", "langchain/langserve"))
        # prepare args
        stdin = langgraph_cli.docker.compose(port=port)
        args = [
            "--project-directory",
            config.parent,
            "-f",
            "-",  # stdin
        ]
        # apply options
        if docker_compose:
            args.extend(["-f", str(docker_compose)])
        args.append("up")
        if config:
            with open(config) as f:
                stdin += langgraph_cli.config.config_to_compose(config, json.load(f))
        if recreate:
            args.extend(["--force-recreate", "--remove-orphans"])
            shutil.rmtree(".langserve-data", ignore_errors=True)
        # run docker compose
        runner.run(exec("docker", "compose", *args, input=stdin))


@OPT_O
@OPT_PORT
@cli.command()
def watch(override: pathlib.Path, port: int):
    compose = langgraph_cli.docker.compose(port=port)

    with asyncio.Runner() as runner:
        try:
            runner.run(
                gather(
                    exec(
                        "docker",
                        "compose",
                        "--project-directory",
                        override.parent,
                        "-f",
                        "-",
                        "-f",
                        str(override),
                        "watch",
                        input=compose,
                    ),
                    exec_loop(
                        "docker",
                        "compose",
                        "--project-directory",
                        override.parent,
                        "-f",
                        "-",
                        "-f",
                        str(override),
                        "logs",
                        "--follow",
                        "--since",
                        PLACEHOLDER_NOW,
                        "langserve",
                        input=compose,
                    ),
                )
            )
        finally:
            # docker compose watch doesn't clean up on exit, so we need to do it
            runner.run(
                exec(
                    "docker",
                    "compose",
                    "--project-directory",
                    override.parent,
                    "-f",
                    "-",
                    "-f",
                    str(override),
                    "kill",
                    input=compose,
                )
            )
