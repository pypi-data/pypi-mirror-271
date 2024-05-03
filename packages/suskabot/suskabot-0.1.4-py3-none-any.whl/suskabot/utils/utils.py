def get_formatted_progressbar(video_title: str, progress_percentage: int) -> str:
    blank_symbol = "▯ "
    filled_symbol = "▮ "
    total_symbols_number = 10

    filled_symbols_number = progress_percentage // total_symbols_number
    blank_symbols_number = total_symbols_number - filled_symbols_number

    progressbar: str = \
        (f"Downloading {video_title}..\n"
         f"{filled_symbol * filled_symbols_number}{blank_symbol * blank_symbols_number}{progress_percentage}%")

    return progressbar


def get_download_progress_percentage(total_bytes: int, remaining_bytes: int) -> int:
    return int(((total_bytes - remaining_bytes) / total_bytes) * 100)


def pytube_video_resolution_to_int(resolution: str) -> int:
    return int(resolution[0:-1])


def bytes_to_megabytes(bytes_number: int) -> int:
    return int(bytes_number / 1000 / 1000)
