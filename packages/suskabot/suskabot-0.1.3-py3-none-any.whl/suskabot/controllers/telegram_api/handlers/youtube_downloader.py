import asyncio
import logging
import concurrent.futures
from asyncio import AbstractEventLoop
from typing import  Set

import telegram.error
from pytube import Stream
from pytube.exceptions import RegexMatchError, VideoUnavailable, PytubeError
from telegram import Update, Message
from telegram.ext import ContextTypes, Application, MessageHandler, filters

from suskabot.services.youtube_downloader import YTDownloaderService, VideoTooLarge

from suskabot.utils.utils import get_download_progress_percentage, get_formatted_progressbar

logger: logging.Logger = logging.getLogger(__name__)


class YTDownloaderHandlers:
    _application: Application
    _yt_downloader_service: YTDownloaderService

    # set of telegram user ids
    _users_with_a_download_in_progress: Set[int] = set()

    _asyncio_loop: AbstractEventLoop = asyncio.get_event_loop()

    def __init__(
            self,
            application: Application,
            downloader_service: YTDownloaderService
    ) -> None:
        self._application = application
        self._yt_downloader_service = downloader_service

        self._application.add_handlers(
            [
                MessageHandler(
                    filters.Regex(r"^(https?\:\/\/)?((www\.)?youtube\.com|youtu\.be)\/.+$"), self.send_yt_video
                ),
            ]
        )

    async def send_yt_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.effective_user.id in self._users_with_a_download_in_progress:
            logger.info(f"{update.effective_user.full_name}, {update.effective_user.id} "
                        "tried to download another video before his previous download finished")
            await update.effective_message.reply_text("Wait for your previous download to finish!")
            return

        video_url: str = update.effective_message.text

        try:
            video_stream: Stream = self._yt_downloader_service.get_youtube_video_stream(video_url)
        except RegexMatchError:
            logger.error(f"{video_url} doesnt look like a valid url, sussy baka: {update.effective_user.full_name}")
            await update.effective_message.reply_text("Check video url")
            return
        except VideoUnavailable as e:
            logger.error(f"{video_url} is not available, {e}")
            await update.effective_message.reply_text(f"The video is not available, {e}")
            return
        except VideoTooLarge as e:
            logger.error(f"Video too larger error, {e}")
            await update.effective_message.reply_text(f"Video too larger error, {e}")
            return

        progressbar: str = get_formatted_progressbar(video_stream.title, 0)
        progressbar_message: Message = await update.effective_message.reply_text(progressbar)

        self._users_with_a_download_in_progress.add(update.effective_user.id)
        logger.debug(f"Added {update.effective_user.id} to the set of downloading user, "
                     f"current set:{self._users_with_a_download_in_progress}")

        async def _clean_up():
            await progressbar_message.delete()
            self._users_with_a_download_in_progress.remove(update.effective_user.id)
            logger.debug(f"Successfully deleted the progressbar and "
                         f"Removed {update.effective_user.id} from the set of downloading user, "
                         f"current set:{self._users_with_a_download_in_progress}")

        def download_progress_callback(stream: Stream, b: bytes, remaining_bytes: int) -> None:
            logger.debug(f"Got a progress callback for {update.effective_user.full_name} {update.effective_user.id}, "
                         f"{remaining_bytes=}")
            del stream, b  # unused for current implementation of the callback

            progress_percentage: int = get_download_progress_percentage(
                video_stream.filesize,
                remaining_bytes
            )

            updated_progressbar: str = get_formatted_progressbar(
                video_stream.title,
                progress_percentage
            )

            asyncio.run_coroutine_threadsafe(
                context.bot.edit_message_text(
                    text=updated_progressbar,
                    chat_id=update.effective_chat.id,
                    message_id=progressbar_message.id
                ),
                self._asyncio_loop
            )

        download_yt_video = self._yt_downloader_service.download_youtube_video_stream
        this_loop = self._asyncio_loop
        with concurrent.futures.ThreadPoolExecutor() as pool:
            logger.debug(f"Spinning up the youtube video downloader thread for "
                         f"{update.effective_user.full_name} {update.effective_user.id}")
            try:
                downloaded_video: bytes | None = await this_loop.run_in_executor(
                    pool,
                    download_yt_video,
                    video_stream,
                    download_progress_callback
                )
            except (OSError, PytubeError) as e:
                await _clean_up()
                logger.error(f"Couldn't download video to disk, {e}")
                await update.effective_message.reply_text("Service error, please try again later")
                return

        await progressbar_message.edit_text("Download complete! Sending the video..")
        logger.debug("Video downloaded, starting to send it")

        try:
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=downloaded_video,
                caption=video_stream.title
            )
        except telegram.error.TelegramError as e:
            logger.error(f"Couldn't send downloaded video, {e}")
            await update.effective_message.reply_text(
                "A Telegram error occurred"
            )
        finally:
            await _clean_up()
