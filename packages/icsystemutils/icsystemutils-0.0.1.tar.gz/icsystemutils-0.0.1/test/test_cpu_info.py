from icsystemutils.cpu.cpu_info import CpuInfo


def test_cpu_info():

    cpu_info = CpuInfo()
    cpu_info.read()
