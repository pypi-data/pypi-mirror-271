from cloud_components.application.interface.services.env.enviroment import (
    IEnviroment,
)
from cloud_components.application.interface.services.log.logger import ILogger
from cloud_components.services.env.dotenv import Dotenv


class EnvFactory:
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def manufacture_dotenv(self) -> IEnviroment:
        return Dotenv(log=self.logger)
