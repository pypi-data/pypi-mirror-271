from telegram.ext import ApplicationBuilder, Application

from suskabot.config.config import Config
from suskabot.controllers.telegram_api.bot import TGBot
from suskabot.services.translator import TranslatorService
from suskabot.services.youtube_downloader import YTDownloaderService


class App:
    _translator_service: TranslatorService
    _youtube_downloader_service: YTDownloaderService

    _ptb_app: Application
    _telegram_bot: TGBot

    def __init__(
            self,
            config: Config
    ) -> None:
        # initialize services
        self._translator_service = TranslatorService(
            comma_separated_translation_services=config.comma_separated_translation_services,
            user_language=config.user_language,
            default_lang_to_translate_to=config.default_language_to_translate_to
        )

        self._youtube_downloader_service = YTDownloaderService(
            file_size_limit_mb=config.file_size_limit_mb,
            min_video_res=config.minimum_video_resolution,
            max_video_res=config.maximum_video_resolution,
            save_to_drive=config.save_to_drive
        )

        # initialize controllers
        self._ptb_app = ApplicationBuilder().token(config.tg_bot_api_token).build()
        self._telegram_bot = TGBot(
            application=self._ptb_app,
            translator_service=self._translator_service,
            yt_downloader_service=self._youtube_downloader_service
        )

    def run(self) -> None:
        self._telegram_bot.start()
