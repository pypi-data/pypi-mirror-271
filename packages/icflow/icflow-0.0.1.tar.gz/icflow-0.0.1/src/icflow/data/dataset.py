from pathlib import Path
import logging

from icsystemutils.network.remote import RemoteHost

from icflow.utils.serialization import Config
from icflow.utils import filesystem as fs


class BaseDataset:
    """
    This class represents a collection of model input data.
    The data can be remote - in which case instances can be
    used to sync with it
    """

    def __init__(self, config: Config) -> None:
        self.name = config.get("name")
        self.archive_name = config.get("archive_name", self.name + ".zip")
        host_name = config.get_child("location", "host")
        self.host: RemoteHost | None = None
        if host_name is not None:
            self.host = RemoteHost(host_name)
        self.location = Path(config.get_child("location", "path"))

    def archive(self, dir: Path):
        archive_name, archive_format = self.archive_name.split(".")
        fs.make_archive(archive_name, archive_format, dir)

    def upload(self, loc: Path):
        archive_path = self._get_archive_path()
        if loc.is_dir():
            logging.info(f"Zipping dataset {self.archive_name}")
            self.archive(loc)
            logging.info(f"Finished zipping dataset {self.archive_name}")
            loc = loc / self.archive_name
        if self.host:
            logging.info(
                f"Uploading {loc} to remote at {self.host.name}:{archive_path}"
            )
            self.host.upload(loc, archive_path)
            logging.info(f"Finished Uploading {loc} to {archive_path}")
        else:
            logging.info(f"Doing local copy of {loc} to {archive_path}")
            fs.copy(loc, archive_path)
            logging.info(f"Finished local copy of {loc} to {archive_path}")

    def download(self, loc: Path):
        archive_path = self._get_archive_path()
        if self.host:
            remote = f"{self.host.name}:{archive_path}"
            logging.info(f"Downloading remote {remote} to {loc}")
            self.host.download(archive_path, loc)
        else:
            logging.info(f"Copying {archive_path} to {loc}")
            fs.copy(archive_path, loc)

        archive_loc = loc / self.archive_name
        logging.info(f"Unpacking {archive_loc} to {loc}")
        fs.unpack_archive(archive_loc, loc)

    def _get_archive_path(self) -> Path:
        return self.location / Path(self.name) / Path(self.archive_name)
