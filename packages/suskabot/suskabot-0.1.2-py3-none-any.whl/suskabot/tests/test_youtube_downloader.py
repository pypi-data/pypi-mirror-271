import gc
import unittest

from pytube.exceptions import RegexMatchError

from suskabot.services.youtube_downloader import YTDownloaderService


class TestYoutubeDownloader(unittest.TestCase):
    min_video_resolution: int = 144
    max_video_resolution: int = 2160
    file_size_limit_mb: int = 10
    save_to_drive: bool = False

    test_video_url: str = "https://www.youtube.com/watch?v=BBJa32lCaaY"
    test_video: bytes

    service: YTDownloaderService

    def setUp(self):
        self.service = YTDownloaderService(
            file_size_limit_mb=self.file_size_limit_mb,
            min_video_res=self.min_video_resolution,
            max_video_res=self.max_video_resolution,
            save_to_drive=self.save_to_drive
        )

        with open("./suskabot/tests/resources/cats.mp4", "rb") as test_file:
            self.test_video = test_file.read()

    def test_correct_downloads(self):
        self.assertEqual(
            self.service.download_youtube_video(self.test_video_url),
            self.test_video
        )

    def test_invalid_url_detection(self):
        self.assertRaises(RegexMatchError, self.service.download_youtube_video, "hehe")

    def tearDown(self):
        del self.service
        gc.collect()


if __name__ == '__main__':
    unittest.main()
