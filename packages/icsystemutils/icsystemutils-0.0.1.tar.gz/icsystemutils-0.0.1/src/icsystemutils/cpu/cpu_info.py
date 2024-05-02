import sys

from .linux_cpu import ProcInfoReader
from .mac_cpu import SysctlCpuReader


class CpuInfo:

    """
    If something fancier is needed there is https://github.com/pytorch/cpuinfo
    """

    def __init__(self) -> None:
        self.physical_procs: dict = {}
        self.threads_per_core = 1
        self.cores_per_node = 1

        if sys.platform == "darwin":
            self.reader = SysctlCpuReader()
        else:
            self.reader = ProcInfoReader()

        self.read()

    def read(self):
        self.reader.read()
        self.refresh()

    def refresh(self):
        if not self.physical_procs:
            return

        # This is assuming all processors have same number of cores
        # and all cores have same number of threads
        self.cores_per_node = len(self.physical_procs.values()[0].cores)
        self.threads_per_core = len(
            self.physical_procs.values()[0].cores.values()[0].threads
        )
