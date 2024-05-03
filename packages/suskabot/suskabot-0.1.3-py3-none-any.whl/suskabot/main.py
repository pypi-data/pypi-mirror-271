import logging
import sys

from typing import Optional
from contextlib import suppress

from config import config

from suskabot.app import app


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    force=True
)
if logging.root.level > logging.DEBUG:
    # prevents log spam from infinite polling
    logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # somehow pydantic raises an attribute error when I'm trying to access config.Config for the type hint
    # removing the type hint solves the issue, but I'd rather just suppress the pydantic error
    with suppress(AttributeError):
        config: Optional[config.Config] = config.load_config()
    if not config:
        logger.error("Couldn't load config file")
        sys.exit(1)

    app = app.App(config)

    app.run()


# if __name__ == '__main__':
#     try:
#         config: Optional[config.Config] = config.load_config()
#     except AttributeError:
#         # somehow pydantic raises an attribute error when trying to access config.Config for the type hint
#         # removing the type hint solves the issue, but I'd rather just suppress the pydantic error
#         pass
#     if not config:
#         logger.error("Couldn't load config file")
#         sys.exit(1)
#
#     # services
#     translation_service = translator.TranslatorService(
#         comma_separated_translation_services=config.comma_separated_translation_services,
#         user_language=config.user_language,
#         default_lang_to_translate_to=config.default_language_to_translate_to
#     )
#     logger.debug("Successfully instantiated translation service")
#
#     yt_downloader_service = youtube_downloader.YTDownloaderService(
#         file_size_limit_mb=config.file_size_limit_mb,
#         min_video_res=config.minimum_video_resolution,
#         max_video_res=config.maximum_video_resolution,
#         save_to_drive=config.save_to_drive
#     )
#     logger.debug("Successfully instantiated youtube downloader service")
#
#     # controllers
#     app: telegram.ext.Application = (telegram.ext.ApplicationBuilder()
#                                      .token(config.tg_bot_api_token)
#                                      .concurrent_updates(True)
#                                      .media_write_timeout(60)
#                                      .build()
#                                      )
#     logger.debug("Successfully instantiated python-telegram-bot application")
#
#     tg_bot = bot.TGBot(
#         application=app,
#         translator_service=translation_service,
#         yt_downloader_service=yt_downloader_service
#     )
#     logger.debug("Successfully instantiated suskabot application")
#
#     tg_bot.start()
