from pydantic_settings import SettingsConfigDict
from aau_ais_utilities.connections import EngineSettings
from sqlalchemy import create_engine, Engine
from functools import lru_cache


class DIPAALEngineSettings(EngineSettings):
    model_config = SettingsConfigDict(env_prefix='DIPAAL_')


@lru_cache
def get_dipaal_engine() -> Engine:
    return create_engine(DIPAALEngineSettings().url)