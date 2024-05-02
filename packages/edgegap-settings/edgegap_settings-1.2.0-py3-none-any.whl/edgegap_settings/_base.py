from pydantic_settings import BaseSettings

from ._apm import ApmSettings
from ._factory import SettingsFactory
from ._fields import ConsulField
from ._logstash import LogStashSettings


class ProjectBaseSettings(BaseSettings):
    name: str = ConsulField(key='NAME', description='The name of the project')
    host: str = ConsulField(key='HOST', default='localhost', description='The host address of the project')
    port: int = ConsulField(key='PORT', default=5000, description='The port of the project')
    debug: bool = ConsulField(key='DEBUG', default=False, description='Enable debugging for project')
    enabled: bool = ConsulField(key='ENABLED', default=True, description='If the project is Enabled (Deprecated)')
    apm: ApmSettings = SettingsFactory.from_settings(ApmSettings)
    logstash: LogStashSettings = SettingsFactory.from_settings(LogStashSettings)
