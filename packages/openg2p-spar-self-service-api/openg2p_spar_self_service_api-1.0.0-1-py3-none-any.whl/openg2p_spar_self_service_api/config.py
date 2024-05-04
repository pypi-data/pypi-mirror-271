from openg2p_fastapi_auth.config import ApiAuthSettings
from openg2p_fastapi_auth.config import Settings as AuthSettings
from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(AuthSettings, BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="spar_selfservice_", env_file=".env", extra="allow"
    )

    openapi_title: str = "SPAR Self Service API"
    openapi_description: str = """
    SPAR Self Service API
    ***********************************
    Further details goes here
    ***********************************
    """
    openapi_version: str = __version__

    db_dbname: str = "openg2p_spar_db"

    auth_api_test_strategy: ApiAuthSettings = ApiAuthSettings(enabled=True)
    auth_api_link: ApiAuthSettings = ApiAuthSettings(enabled=True)
    auth_api_unlink: ApiAuthSettings = ApiAuthSettings(enabled=True)
    auth_api_update: ApiAuthSettings = ApiAuthSettings(enabled=True)
    auth_api_resolve: ApiAuthSettings = ApiAuthSettings(enabled=True)
    auth_api_get_dfsp_level: ApiAuthSettings = ApiAuthSettings(enabled=True)
    auth_api_api_get_dfsp_level_values: ApiAuthSettings = ApiAuthSettings(enabled=True)

    mapper_api_url: str = "http://localhost:8007/sync"
    mapper_api_timeout: int = 60
    mapper_link_path: str = "/link"
    mapper_update_path: str = "/update"
    mapper_resolve_path: str = "/resolve"
    mapper_unlink_path: str = "/unlink"
