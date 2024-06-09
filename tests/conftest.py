# ruff: noqa: SIM117
import contextlib
import os
import secrets
import socket
import time

import pytest

from transmission_rpc import LOGGER
from transmission_rpc.client import Client

HOST = os.getenv("TR_HOST", "127.0.0.1")
PORT = int(os.getenv("TR_PORT", "9091"))
USER = os.getenv("TR_USER", "admin")
PASSWORD = os.getenv("TR_PASSWORD", "password")


def pytest_configure():
    start = time.time()
    while True:
        with contextlib.suppress(ConnectionError):
            with socket.create_connection((HOST, PORT), timeout=5):
                break

        if time.time() - start > 30:
            print()


@pytest.fixture()
def tr_client():
    LOGGER.setLevel("INFO")
    with Client(host=HOST, port=PORT, username=USER, password=PASSWORD) as c:
        for torrent in c.get_torrents():
            c.remove_torrent(torrent.id, delete_data=True)
        yield c
        for torrent in c.get_torrents():
            c.remove_torrent(torrent.id, delete_data=True)


@pytest.fixture()
def fake_hash_factory():
    return lambda: secrets.token_hex(20)
