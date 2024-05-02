import logging
import os
import sys
from typing import Any

from dotenv import load_dotenv
from edgegap_consul import ConsulReader, ConsulReaderFactory
from edgegap_logging import DefaultFormatter
from pydantic import ValidationError
from pydantic_settings import BaseSettings

load_dotenv()

logger = logging.getLogger('settings.Factory')

# Small Temporary formatting since this is most likely be called before any Logger Initialization
fmt = DefaultFormatter()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(fmt)
logger.addHandler(handler)


class SettingsFactory:
    __mapping__: dict[str, type(BaseSettings)] = {}
    __consul_reader: ConsulReader = ConsulReaderFactory().from_env()

    @classmethod
    def from_settings(cls, settings: type(BaseSettings)) -> type(BaseSettings):
        name = settings.__name__

        if name not in cls.__mapping__.keys():
            consul_prefix = settings.model_config.get('prefix')
            data = {}

            for field_name, field in settings.model_fields.items():
                if isinstance(field.json_schema_extra, dict):
                    consul_key = field.json_schema_extra.get('consul_key')
                    env_key = field.json_schema_extra.get('env_key')
                    value = None

                    # Check if in Environment Variable First
                    if isinstance(env_key, str):
                        value = os.environ.get(env_key, field.default)

                    # Consul Override Environment Variable
                    if isinstance(consul_prefix, str) and isinstance(consul_key, str):
                        consul_full_key = f'{consul_prefix}/{consul_key}'
                        value = cls.__from_consul(consul_full_key, field.default)

                    if value is not None:
                        data[field_name] = value

            try:
                cls.__mapping__[name] = settings(**data)
            except ValidationError as e:
                raise Exception('There was some errors during the Validation of your Settings, please adjust') from e

        return cls.__mapping__.get(name)

    @classmethod
    def __from_consul(cls, consul_full_key: str, default: Any = None) -> Any:
        exists, value = cls.__consul_reader.get(key=consul_full_key)
        has_default = default is not None
        has_value = value is not None

        if has_value:
            return value
        elif not has_value and has_default:
            if exists:
                logger.warning(
                    f'Key [{consul_full_key}] defined in Consul but the value was None,'
                    f" will fallback to default value '{default}'",
                )
            else:
                logger.warning(
                    f'Key [{consul_full_key}] does not exists in Consul but ' f"default is defined to: '{default}'",
                )
        else:
            raise Exception(f'Consul key [{consul_full_key}] is not defined and no default value')
