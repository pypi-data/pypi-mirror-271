# stream_downloader
Download a stream by m3u8 file.

## Prerequisites
This library requires `ffmpeg` to be previously installed on your machine.
Detailed instructions on `ffmpeg` installation can be found [here](https://ffmpeg.org/download.html).

## Install package from PyPi
```cmd
pip install stream_downloader
```

## Usage
```python
from stream_downloader import download

download(
    playlist_url="https://my-video-hosting.com/id/manifest.m3u8",
    headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"},
    video_channel=0,
    audio_channel=0,
    destination_file="my_videos/video.mp4",
)
```
