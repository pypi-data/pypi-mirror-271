import subprocess
from pathlib import Path

from .cpu import PhysicalProcessor


class SysctlCpuReader:
    def __init__(self) -> None:
        self.sysctl_path = Path("/usr/sbin/sysctl")

    def read_sysctl_key(self, key: str):
        # https://man.freebsd.org/cgi/man.cgi?sysctl(8)
        ret = subprocess.check_output([str(self.sysctl_path), key])
        return ret.decode("utf-8").strip()

    def read(self):
        machdep_cpu = self.read_sysctl_key("machdep.cpu")
        return self._parse_machdep_cpu(machdep_cpu)

    def get_key_value(self, line: str):
        key, value = line.split(":")
        return key.strip(), value.strip()

    def _parse_machdep_cpu(self, content: str):
        dict = {}
        for line in content.splitlines():
            key, value = self.get_key_value(line)
            key_no_prefix = key[len("machdep.cpu") :]
            dict[key_no_prefix] = value

        proc = PhysicalProcessor("0")
        if "brand_string" in dict:
            proc.model = dict["brand_string"]

        core_count = 1
        if "core_count" in dict:
            core_count = int(dict["core_count"])

        for idx in range(core_count):
            proc.add_core(str(idx))

        thread_count = 1
        if "thread_count" in dict:
            thread_count = int(dict["thread_count"])
        threads_per_core = int(thread_count / core_count)
        for core in proc.cores.values():
            for idx in range(threads_per_core):
                core.add_thread(idx)
        return {"0": proc}
