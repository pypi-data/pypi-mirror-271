# ruff: noqa: E402

import asyncio

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer

from .controllers import DfspController, SelfServiceController
from .models import DfspLevel, DfspLevelValue, LoginProvider, Strategy


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize(**kwargs)
        DfspController().post_init()
        SelfServiceController().post_init()

    def migrate_database(self, args):
        super().migrate_database(args)

        async def migrate():
            await DfspLevel.create_migrate()
            await DfspLevelValue.create_migrate()
            await Strategy.create_migrate()
            await LoginProvider.create_migrate()

        asyncio.run(migrate())
