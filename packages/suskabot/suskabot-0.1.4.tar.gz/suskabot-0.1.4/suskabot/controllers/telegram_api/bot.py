import logging

from telegram.ext import Application

from controllers.telegram_api.handlers.app import AppHandlers
from controllers.telegram_api.handlers.translator import TranslatorHandlers
from controllers.telegram_api.handlers.youtube_downloader import YTDownloaderHandlers
from services.translator import TranslatorService
from services.youtube_downloader import YTDownloaderService


logger: logging.Logger = logging.getLogger(__name__)


class TGBot:
    _application: Application
    _translator_service: TranslatorService
    _yt_downloader_service: YTDownloaderService

    def __init__(
            self,
            application: Application,
            translator_service: TranslatorService,
            yt_downloader_service: YTDownloaderService,
    ) -> None:
        self._application = application
        self._translator_service = translator_service
        self._yt_downloader_service = yt_downloader_service

        AppHandlers(self._application)
        logger.debug("Successfully applied application handlers")

        YTDownloaderHandlers(self._application, self._yt_downloader_service)
        logger.debug("Successfully applied youtube downloader handlers")

        TranslatorHandlers(self._application, self._translator_service)
        logger.debug("Successfully applied translator handlers")

    def start(self) -> None:
        logger.debug("Starting TG bot application..")
        self._application.run_polling()
