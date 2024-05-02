class ProcessorThread:
    def __init__(self, id: str) -> None:
        self.id = id


class ProcessorCore:
    def __init__(self, id: str) -> None:
        self.id = id
        self.threads: dict = {}

    def add_thread(self, id: str):
        self.threads[id] = ProcessorThread(id)


class PhysicalProcessor:
    def __init__(self, id: str) -> None:
        self.id = id
        self.cores: dict = {}
        self.model = ""
        self.cache_size = 0
        self.cpu_cores = 1
        self.siblings = 1

    def add_core(self, id: str):
        self.cores[id] = ProcessorCore(id)
