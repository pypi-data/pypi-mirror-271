from pathlib import Path

from .cpu import PhysicalProcessor


class ProcInfoReader:
    def __init__(self, path: None | Path = None) -> None:
        if path:
            self.path = path
        else:
            self.path = Path("/proc/cpuinfo")
        self.init()

    def init(self):
        self.blocks = []
        self.processors = {}

    def get_key_value(self, line):
        key, value = line.split(":")
        return key.strip(), value.strip()

    def read_block(self, content):
        offset = 0

        block = {}
        for line in content:
            stripped_line = line.strip()
            if not stripped_line:
                break
            key, value = self.get_key_value(stripped_line)
            block[key] = value
            offset += 1

        if offset > 0:
            self.blocks.append(block)
        return offset + 1

    def _on_new_physical_proc(self, id, block):
        proc = PhysicalProcessor(id)
        if "model name" in block:
            proc.model = block["model name"]
        if "cache size" in block:
            proc.cache_size = block["cache size"]
        if "siblings" in block:
            self.siblings = int(block["siblings"])
        if "cpu cores" in block:
            self.cpu_cores = int(block["cpu cores"])
        self.processors[id] = proc

    def _on_new_core(self, physical_id, core_id):
        self.processors[physical_id].add_core(core_id)

    def on_new_thread(self, physical_id, core_id, thread_id):
        self.processors[physical_id].cores[core_id].add_thread(thread_id)

    def _populate_processors(self):
        for block in self.blocks:
            if "physical id" in block:
                physical_id = block["physical id"]
            else:
                physical_id = 0
            if physical_id not in self.processors:
                self._on_new_physical_proc(physical_id, block)

            if "core id" in block:
                core_id = block["core id"]
            else:
                core_id = 0
            if core_id not in self.processors[physical_id].cores:
                self._on_new_core(physical_id, core_id)

            if "processor" in block:
                processor_id = block["processor"]
            else:
                processor_id = 0
            threads = self.processors[physical_id].cores[core_id].threads
            if processor_id not in threads:
                self.on_new_thread(physical_id, core_id, processor_id)

    def read(self, content=None):
        self.init()

        if not content:
            with open(self.path, "r") as f:
                content = f.readlines()

        offset = 0
        while offset < len(content):
            offset += self.read_block(content[offset:])

        self._populate_processors()
        return self.processors
