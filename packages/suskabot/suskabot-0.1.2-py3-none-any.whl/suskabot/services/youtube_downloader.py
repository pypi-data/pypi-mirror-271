import functools
import os
import logging
import pathlib
import shutil
from io import BytesIO

from typing import Optional, Callable

from pytube.exceptions import PytubeError
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

        video_stream: Stream
        for video_stream in ordered_video_streams:
            video_resolution: int = pytube_video_resolution_to_int(video_stream.resolution)
            video_filesize_mb: int = bytes_to_megabytes(video_stream.filesize)

            # noinspection PyChainedComparisons
            # I don't like how chained comparisons look.
            if (video_filesize_mb <= self._FILE_SIZE_LIMIT_MB and
                    video_resolution >= self._MINIMUM_VIDEO_RESOLUTION and
                    video_resolution <= self._MAXIMUM_VIDEO_RESOLUTION):
                return video_stream
        else:
            return None

    # all the stream availability exceptions are raised here!
    def get_youtube_video_stream_metadata(self, video_url: str) -> Optional[YTVideoMetadata]:
        try:
            video_data = YouTube(url=video_url)
            video_data.check_availability()
        except RegexMatchError as e:
            raise e
        except VideoUnavailable as e:
            raise e

        progressive_video_streams: StreamQuery = video_data.streams.filter(progressive=True)

        video_stream: Stream | None = self.__get_best_quality_stream_under_limits(progressive_video_streams)
        if not video_stream:
            raise VideoTooLarge(f"Can't download videos larger than {self._FILE_SIZE_LIMIT_MB}MB")

        metadata = YTVideoMetadata(
            title=video_data.title,
            filesize_bytes=video_stream.filesize
        )

        return metadata

    # here it is assumed that the best video stream under limits is ready to be downloaded
    def download_youtube_video(
            self,
            video_url: str,
            progress_callback: Callable[[Stream, bytes, int], None] | None = None
    ) -> bytes | None:
        if progress_callback:
            video_data = YouTube(
                url=video_url,
                on_progress_callback=progress_callback
            )
        else:
            video_data = YouTube(url=video_url)

        progressive_video_streams: StreamQuery = video_data.streams.filter(progressive=True)

        video_stream: Stream = self.__get_best_quality_stream_under_limits(progressive_video_streams)

        if self._SAVE_TO_DRIVE:
            video_path: str = video_stream.download(
                output_path=str(self._DEFAULT_DOWNLOAD_PATH)
            )
        else:
            with BytesIO() as buffer:
                video_stream.stream_to_buffer(buffer)
                logger.info(f"Successfully downloaded {video_url} to RAM")
                return buffer.getvalue()

        with open(video_path, "rb") as video_file:
            logger.info(f"Successfully downloaded {video_url} to drive")
            return video_file.read()

    # doesn't serve any purpose as of now, but I'll leave it here for a bit
    def __clear_download_directory(self) -> None:
        try:
            shutil.rmtree(self._DEFAULT_DOWNLOAD_PATH)
        except Exception as e:
            logger.warning(f"Could not clear download directory, {e}")
            raise e
