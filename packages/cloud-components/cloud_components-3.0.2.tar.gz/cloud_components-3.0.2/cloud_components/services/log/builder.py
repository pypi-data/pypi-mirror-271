from typing import cast
from cloud_components.application.interface.services.log.logger import ILogger


class LogBuilder:
    def build_loguru(self) -> ILogger:
        from loguru import logger  # pylint: disable=C0415

        return cast(ILogger, logger)
