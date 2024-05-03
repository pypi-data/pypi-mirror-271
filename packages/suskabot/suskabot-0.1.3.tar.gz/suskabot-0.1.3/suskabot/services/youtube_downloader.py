import os
import logging
import pathlib
import shutil
from io import BytesIO

from typing import Optional, Callable

from pytube import YouTube, StreamQuery, Stream
from pytube.exceptions import RegexMatchError, VideoUnavailable

from suskabot.utils.utils import pytube_video_resolution_to_int, bytes_to_megabytes

logger: logging.Logger = logging.getLogger(__name__)


class VideoTooLarge(Exception):
    """Raise if a video file size exceeds set limits"""


class YTVideoMetadata:
    title: str
    filesize_bytes: int

    def __init__(
            self,
            title: str,
            filesize_bytes: int,
    ) -> None:
        self.title = title
        self.filesize_bytes = filesize_bytes


class YTDownloaderService:
    _MINIMUM_VIDEO_RESOLUTION: int
    _MAXIMUM_VIDEO_RESOLUTION: int
    _FILE_SIZE_LIMIT_MB: int
    _SAVE_TO_DRIVE: bool

    _DEFAULT_DOWNLOAD_PATH = pathlib.Path(os.getcwd()).joinpath("yt_downloads/")

    def __init__(
            self,
            min_video_res: int,
            max_video_res: int,
            file_size_limit_mb: int,
            save_to_drive: bool
    ) -> None:
        self._MINIMUM_VIDEO_RESOLUTION = min_video_res
        self._MAXIMUM_VIDEO_RESOLUTION = max_video_res
        self._FILE_SIZE_LIMIT_MB = file_size_limit_mb
        self._SAVE_TO_DRIVE = save_to_drive

    def __get_best_quality_stream_under_limits(self, video_streams: StreamQuery) -> Optional[Stream]:
        ordered_video_streams: StreamQuery = video_streams.order_by("resolution").desc()
        logger.debug(f"Trying to find a stream under {self._FILE_SIZE_LIMIT_MB} MB, between "
                     f"{self._MINIMUM_VIDEO_RESOLUTION}p and {self._MAXIMUM_VIDEO_RESOLUTION}p")

        video_stream: Stream
        for video_stream in ordered_video_streams:
            video_resolution: int = pytube_video_resolution_to_int(video_stream.resolution)
            video_filesize_mb: int = bytes_to_megabytes(video_stream.filesize)
            logger.debug(f"Checking a stream {video_stream.itag} with {video_stream.resolution} resolution "
                         f"and {video_filesize_mb} MB filesize")
            # noinspection PyChainedComparisons
            # I don't like how chained comparisons look.
            if (video_filesize_mb <= self._FILE_SIZE_LIMIT_MB and
                    video_resolution >= self._MINIMUM_VIDEO_RESOLUTION and
                    video_resolution <= self._MAXIMUM_VIDEO_RESOLUTION):
                logger.debug(f"Selected stream {video_stream.itag}")
                return video_stream
        else:
            logger.debug("No video stream fits the requirements")
            return None

    # all the stream availability exceptions are raised here!
    def get_youtube_video_stream(self, video_url: str) -> Optional[Stream]:
        try:
            video_data = YouTube(url=video_url)
            video_data.check_availability()
        except RegexMatchError as e:
            raise e
        except VideoUnavailable as e:
            raise e

        progressive_video_streams: StreamQuery = video_data.streams.filter(progressive=True)
        logger.debug(f"Found progressive streams:\n{progressive_video_streams}")

        video_stream: Stream | None = self.__get_best_quality_stream_under_limits(progressive_video_streams)
        logger.debug(f"Selected video stream:\n{video_stream}")

        if not video_stream:
            raise VideoTooLarge(f"Can't download videos larger than {self._FILE_SIZE_LIMIT_MB}MB")

        return video_stream

    def download_youtube_video_stream(
            self,
            video_stream: Stream,
            progress_callback: Callable[[Stream, bytes, int], None] | None = None
    ) -> bytes | None:
        # the only way to register a callback is at the moment of YouTube object creation.
        # since this function only has a stream object to work with,
        # registering a callback is impossible by normal means.
        # one more reason to migrate from pytube, lol
        video_stream._monostate.on_progress = progress_callback

        if self._SAVE_TO_DRIVE:
            video_path: str = video_stream.download(
                output_path=str(self._DEFAULT_DOWNLOAD_PATH)
            )
        else:
            with BytesIO() as buffer:
                video_stream.stream_to_buffer(buffer)
                logger.info(f"Successfully downloaded {video_stream.url} to RAM")
                return buffer.getvalue()

        with open(video_path, "rb") as video_file:
            logger.info(f"Successfully downloaded {video_stream.url} to drive")
            return video_file.read()

    # doesn't serve any purpose as of now, but I'll leave it here for a bit
    def __clear_download_directory(self) -> None:
        try:
            shutil.rmtree(self._DEFAULT_DOWNLOAD_PATH)
        except Exception as e:
            logger.warning(f"Could not clear download directory, {e}")
            raise e
