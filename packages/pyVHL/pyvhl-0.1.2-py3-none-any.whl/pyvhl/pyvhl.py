import os
import random

from requests import Session
from retry import retry
from pyvhl.mirror_clients import Client
from youtube_dl import YoutubeDL
from loguru import logger


class pyvhl:
    """
    Handles proccessing of mirroring videos from Reddit and Twitter.
    """

    def __init__(self) -> None:
        session = Session()
        session.headers["User-Agent"] = "pyVHL/0.1.2"
        self.client = Client(session=session)
        self.clients = {
            "streamable": self.client.streamable,
            "catbox": self.client.catbox,
        }

    @retry(delay=5, tries=5)
    def get_video(self, video_url: str, download: bool = True) -> dict:
        """Get video and video information

        Args:
            video_url (str):
            download (bool, optional): [description]. Defaults to True.

        Returns:
            dict: Contains video information
        """
        youtube_dl_opts = {
            "quiet": True,
            "outtmpl": "%(id)s.%(ext)s",
        }
        with YoutubeDL(youtube_dl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=download)

        # get size of file downloaded
        if download:
            file_size = os.stat(info_dict["id"] + "." + info_dict["ext"]).st_size

        if info_dict["extractor"] == "twitch:clips":
            clip_title = info_dict["title"]
            clip_url = info_dict["formats"][-1]["url"]
            clip_id = info_dict["id"]
            clip_streamer = info_dict["creator"]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
                "file_size": file_size,
            }
            # return clip_title, clip_url, clip_id, clip_streamer

        elif info_dict["extractor"] == "youtube":
            clip_title = info_dict["title"]
            clip_url = info_dict["webpage_url"]
            clip_id = info_dict["id"]
            clip_streamer = video_url.split("/")[3]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
                "file_size": file_size,
            }

        elif info_dict["extractor"] == "facebook":
            info_dict = info_dict["entries"][-1]
            clip_title = info_dict["title"]
            clip_url = info_dict["url"]
            clip_id = info_dict["id"]
            clip_streamer = video_url.split("/")[3]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
                "file_size": file_size,
            }

        elif info_dict["extractor"] == "fb":
            info_dict = info_dict["entries"][-1]
            clip_title = info_dict["title"]
            clip_url = info_dict["url"]
            clip_id = info_dict["id"]
            clip_streamer = video_url.split("/")[3]
            clip_date = info_dict["upload_date"]
            extractor = info_dict["extractor"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "extractor": extractor,
            }

        elif info_dict["extractor"] == "generic":
            clip_title = info_dict["title"]
            clip_url = info_dict["webpage_url"]
            clip_id = info_dict["id"]
            clip_streamer = info_dict["uploader"]
            clip_date = info_dict["upload_date"]
            return {
                "title": clip_title,
                "url": clip_url,
                "id": clip_id,
                "streamer": clip_streamer,
                "date": clip_date,
                "file_size": file_size,
            }

        else:
            logger.error(f"Clip URL: {video_url} | Clip not available")
            return {"title": None, "url": None, "id": None, "streamer": None, "date": None, "file_size": None}

    @retry(tries=10, delay=5)
    def upload_video(self, clip_title: str, id: int, host: str = "") -> dict:
        """Uploads clip to one of the mirror clients

        Args:
            clip_title (str): Clip title
            id (int): Clip id

        Returns:
            str: Mirror url
        """
        if host not in ["streamable", "catbox"]:
            raise ValueError("Invalid host, must be either 'streamable' or 'catbox'")
        if host:
            client = self.clients[host]
        else:
            client_name = random.choice(list(self.clients.keys()))
            client = self.clients[client_name]
        for file in os.listdir("./"):
            if file.endswith(".mp4"):
                if file.startswith(str(id)):
                    clip_file = file
                    break
        try:
            with open(clip_file, "rb") as f:
                mirror = client.upload_video(f, f"{id}.mp4")
        finally:
            # remove file
            os.remove(clip_file)

        return {"mirror_url": mirror.url, "host": client_name}
