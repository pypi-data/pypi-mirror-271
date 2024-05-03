import logging
import os
from typing import Self, Dict, Optional

import telegram.constants
import pydantic
import dotenv

from suskabot.utils import utils


logger = logging.getLogger(__name__)


POSSIBLE_VIDEO_RESOLUTIONS = [
    144,
    240,
    360,
    480,
    720,
    1080,
    1440,
    2160
]


class Config(pydantic.BaseModel):
    tg_bot_api_token: str = pydantic.Field(pattern=r"^[0-9]{8,10}:[a-zA-Z0-9_-]{35}$")

    comma_separated_translation_services: str = pydantic.Field(
        default="google,yandex,bing,argos",
        pattern=r"^([a-zA-Z]+,?)+"
    )
    user_language: str = pydantic.Field(
        default="ru",
        pattern=r"^[^-]{2,3}(-[^-]{2,3})?(-[^-]{2,3})?$"
    )
    default_language_to_translate_to: str = pydantic.Field(
        default="en",
        pattern=r"^[^-]{2,3}(-[^-]{2,3})?(-[^-]{2,3})?$",
    )

    # right now only progressive videos are supported, so video quality is 720p max.
    # it also looks like 360p and 720p are the only available options
    minimum_video_resolution: int = POSSIBLE_VIDEO_RESOLUTIONS[0]
    maximum_video_resolution: int = POSSIBLE_VIDEO_RESOLUTIONS[-1]

    @pydantic.field_validator("maximum_video_resolution", "minimum_video_resolution")
    def validate_option(cls, v):
        assert v in POSSIBLE_VIDEO_RESOLUTIONS, ("this does not look like a valid resolution. "
                                                 f"supported resolutions: {POSSIBLE_VIDEO_RESOLUTIONS}")
        return v

    @pydantic.model_validator(mode='after')
    def check_if_valid_video_resolution_preferences(self) -> Self:
        if self.minimum_video_resolution > self.maximum_video_resolution:
            raise ValueError("minimum video resolution can't be higher than maximum video resolution")
        if self.minimum_video_resolution > 720:
            logger.warning("Since only progressive videos are supported right now,"
                           " 720p is the maximum possible resolution")
        return self

    # setting the limit higher than the default will break telegram api controller!
    file_size_limit_mb: int = pydantic.Field(
        default=utils.bytes_to_megabytes(
            telegram.constants.FileSizeLimit.FILESIZE_UPLOAD.value
        ),
        gt=0,
        validate_default=True
    )

    save_to_drive: bool = pydantic.Field(
        default=True
    )

    # TODO: having a config for yt video downloads directory seems like a nice idea


def load_config() -> Optional[Config]:
    if not os.path.exists("./suskabot/config/.env.secret"):
        with open("./suskabot/config/.env.secret", "w") as f:
            f.write("TG_BOT_API_TOKEN=")
        logger.info("Created .env.secret file")

    public_env_file_config: Dict[str, str | None] = dotenv.dotenv_values("./suskabot/config/.env.public")

    secret_env_file_config: Dict[str, str | None] = dotenv.dotenv_values("./suskabot/config/.env.secret")

    config_data: Dict[str, str | None] = {}
    # it is assumed that every valid configuration is type annotated
    # I tried really hard, but there's no easier way to achieve the same functionality without repeating config names
    configurations: set[str] = vars(Config)['__annotations__'].keys()
    configuration: str
    for configuration in configurations:
        configuration_value: str | None
        configuration_upper = configuration.upper()
        logger.debug(f"Getting {configuration}..")
        if configuration_upper in os.environ:
            configuration_value = os.environ[configuration_upper]
            logger.debug(f"Got {configuration} from environ")
        elif configuration_upper in secret_env_file_config:
            configuration_value = secret_env_file_config[configuration_upper]
            logger.debug(f"Got {configuration} from env.secret")
        elif configuration_upper in public_env_file_config:
            configuration_value = public_env_file_config[configuration_upper]
            logger.debug(f"Got {configuration} from env.public")
        else:
            logger.debug(f"Couldn't find {configuration} anywhere, will try to use the default value")
            continue

        config_data[configuration] = configuration_value
        logger.info(f"{configuration} set to {configuration_value}")

    config: Config = Config(**config_data)

    return config
