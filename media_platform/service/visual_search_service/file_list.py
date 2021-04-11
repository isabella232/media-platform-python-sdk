from __future__ import annotations

from media_platform.lang.serialization import Deserializable
from media_platform.service.file_descriptor import FileDescriptor


class FileList(Deserializable):
    def __init__(self, files: [FileDescriptor]):
        self.files = files

    @classmethod
    def deserialize(cls, data: dict) -> FileList:
        files = [FileDescriptor.deserialize(f) for f in data]
        return FileList(files)
