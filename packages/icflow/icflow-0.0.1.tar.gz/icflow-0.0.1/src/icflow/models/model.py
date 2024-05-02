from pathlib import Path

from icsystemutils.network.remote import RemoteHost


class Model:
    def __init__(self, name, host_name, location, archive_name=None) -> None:
        self.name = name
        self.host = RemoteHost(host_name)
        self.archive_name = archive_name
        self.location = location

    def get_archive_path(self):
        return self.location / Path(self.name) / Path(self.archive_name)

    def upload(self, local_location):
        self.host.upload(local_location, self.get_archive_path())

    def download(self, local_location):
        self.host.download(self.get_archive_path(), local_location)

    def train(self):
        pass
