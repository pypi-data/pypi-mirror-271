from typing import Any

from pydantic import Field


def ConsulField(  # noqa: C901
    key: str = None,
    default: Any = None,
    description: str = None,
    **kwargs,
) -> Any:
    return Field(
        json_schema_extra={'consul_key': key},
        default=default,
        description=description,
        **kwargs,
    )


def EnvironmentField(  # noqa: C901
    key: str,
    description: str = None,
    default: Any = None,
    **kwargs,
):
    return Field(
        json_schema_extra={'env_key': key},
        default=default,
        description=description,
        **kwargs,
    )


def EnvConsulField(  # noqa: C901
    env_key: str,
    consul_key: str,
    description: str = None,
    default: Any = None,
    **kwargs,
):
    return Field(
        json_schema_extra={'env_key': env_key, 'consul_key': consul_key},
        default=default,
        description=description,
        **kwargs,
    )
