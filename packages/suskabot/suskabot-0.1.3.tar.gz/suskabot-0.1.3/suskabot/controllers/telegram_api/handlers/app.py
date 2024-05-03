import logging

from telegram import Update
from telegram.ext import ContextTypes, Application, CommandHandler


logger: logging.Logger = logging.getLogger(__name__)


class AppHandlers:
    _application: Application

    def __init__(self, application: Application) -> None:
        self._application = application

        self._application.add_handlers(
            (
                CommandHandler('start', self.start),
            )
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        greeting_text = "Hi! I'm a Telegram bot that was made to make my creators life easier, " \
                        "here's some of my functionality:\n" \
                        "1) Translator\n" \
                        "English messages will be translated to Russian\n" \
                        "Messages on the any other language will be translated to English\n\n" \
                        "2) YT videos downloader\n" \
                        "Provide a url link to a YouTube video to get mp4 video of it!\n\n" \
                        "3) TBD"

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=greeting_text
        )

        logger.debug(f"Sent the greeting text to {update.effective_user.full_name}, {update.effective_user.id}")
