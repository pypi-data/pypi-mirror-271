import pathlib
from typing import Optional


ROOT = pathlib.Path(__file__).parent.parent.resolve()


DB = f"""
    postgres:
        image: postgres:16
        restart: on-failure
        healthcheck:
            test: pg_isready -U postgres
            start_interval: 1s
            start_period: 5s
            interval: 5s
            retries: 5
        ports:
            - "5433:5432"
        environment:
            POSTGRES_DB: postgres
            POSTGRES_USER: postgres
            POSTGRES_PASSWORD: postgres
        volumes:
            - ./.langserve-data:/var/lib/postgresql/data
            - {ROOT}/initdb:/docker-entrypoint-initdb.d
"""


def compose(
    *,
    # postgres://user:password@host:port/database?option=value
    postgres_uri: Optional[str] = None,
    port: int,
) -> str:
    if postgres_uri is None:
        include_db = True
        postgres_uri = "postgres://postgres:postgres@postgres:5432/postgres?sslmode=disable&search_path=langserve"
    else:
        include_db = False

    return f"""
services:
{DB if include_db else ""}
    migrate:
        image: langchain/langserve-migrate
        pull_policy: always
        {'''depends_on:
            postgres:
                condition: service_healthy''' if include_db else ""}
        environment:
            POSTGRES_URI: {postgres_uri}
    langserve:
        image: langchain/langserve
        restart: on-failure:3
        ports:
            - "{port}:8000"
        depends_on:
            migrate:
                condition: service_completed_successfully
        environment:
            POSTGRES_URI: {postgres_uri}
"""
