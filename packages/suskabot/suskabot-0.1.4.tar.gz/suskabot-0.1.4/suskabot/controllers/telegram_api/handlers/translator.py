import logging

from telegram import Update
from telegram.ext import ContextTypes, Application, MessageHandler, filters
from translators.server import TranslatorError

from services.translator import TranslatorService

logger: logging.Logger = logging.getLogger(__name__)


class TranslatorHandlers:
    _application: Application
    _translator_service: TranslatorService

    def __init__(
            self,
            application: Application,
            translator_service: TranslatorService
    ) -> None:
        self._application = application
        self._translator_service = translator_service

        self._application.add_handlers(
            [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.translate, block=False),
            ]
        )

    async def translate(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        del context  # unused

        text_to_translate: str = update.effective_message.text

        try:
            translation = self._translator_service.translate(text_to_translate)
        except NotImplementedError:
            await update.effective_message.reply_text("Can't translate this language yet :(")
            logger.error(f"couldn't translate \"{text_to_translate}\", couldn't find language to translate to")
            return
        except TranslatorError as e:
            await update.effective_message.reply_text("Service error, please try again later")
            logger.error(f"{e} occured when trying to translate \"{text_to_translate}\"")
            return

        logger.info(f"Successfully sent the translation for \"{text_to_translate}\" "
                    f"to {update.effective_user.full_name}")

        await update.effective_message.reply_text(translation)
