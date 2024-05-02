import subprocess

DEFAULT_HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"
}


def download(
    *,
    playlist_url: str,
    headers: dict = DEFAULT_HEADER,
    program: int = 0,
    video_channel: int = 0,
    audio_channel: int = 0,
    destination_file: str = "video.mp4"
):
    header_args = []
    for header_name, header_value in headers.items():
        header_args.extend(["-headers", f"'{header_name}: {header_value}'"])

    mapping_args = []
    if program:
        mapping_args.extend(["-map", f"0:p:{program}"])
    elif video_channel:
        mapping_args.extend(["-map", f"0:v:{video_channel}"])
    elif audio_channel:
        mapping_args.extend(["-map", f"0:a:{audio_channel}"])
    else:
        mapping_args.extend(["-map", f"0:p:{program}"])

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            *header_args,
            "-i",
            playlist_url,
            *mapping_args,
            destination_file,
        ]
    )
