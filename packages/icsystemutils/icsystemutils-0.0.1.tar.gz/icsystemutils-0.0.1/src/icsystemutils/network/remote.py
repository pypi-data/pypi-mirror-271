from pathlib import Path

import fabric
import fabric.transfer


class RemoteHost:
    """
    Class representing some network location - can
    be used to put or get files to or from that location
    """

    def __init__(self, name) -> None:
        self.name = name
        self.cxn = None | fabric.Connection

    def connect(self):
        if self.cxn is None:
            self.cxn = fabric.Connection(self.name)

    def upload(self, source_path: Path, target_path: Path):
        self.connect()
        transfer = fabric.transfer.Transfer(self.cxn)
        self.cxn.run(f"mkdir -p {target_path.parent}")
        transfer.put(str(source_path), str(target_path))

    def download(self, source_path, target_path):
        self.connect()
        transfer = fabric.transfer.Transfer(self.cxn)
        transfer.get(str(source_path), str(target_path))
