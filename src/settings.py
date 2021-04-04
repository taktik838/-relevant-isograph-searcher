from os import environ
from typing import List

from pydantic.main import BaseModel


class EnvironmentVariables(BaseModel):
    DEBUG: bool
    ENVIRONMENT: str
    SENTRY_DSN: str
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_TECHNICAL_DB: int
    TENSORFLOW_SERVING_TTL_CACHE: int
    TENSORFLOW_SERVING_ENDPOINT: str
    GOOGLE_AUTH_PATH: str
    GOOGLE_TTL_CACHE: int
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    ELASTICSEARCH_INDEX: str


ENV_VARS: EnvironmentVariables = EnvironmentVariables.parse_obj(environ)


APISPEC_CONF: dict = dict(
    title='Isograph searcher',
    version='0.0.1',
    url='/api/swagger.json',
    swagger_path='/api/swagger',
    static_path='/api/swagger/static'
)
