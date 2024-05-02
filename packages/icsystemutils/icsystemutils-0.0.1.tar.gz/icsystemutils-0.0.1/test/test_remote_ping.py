from icsystemutils.network.remote import RemoteHost


def test_remote_host():
    host = RemoteHost("localhost")
    host.connect()
