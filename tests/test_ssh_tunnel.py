"""Tests standard tap features using the built-in SDK tests library."""

import logging
from pathlib import Path

import paramiko
from tap_mysql.tap import TapMySQL

TABLE_NAME = "test_replication_key"
SAMPLE_CONFIG = {
    "sqlalchemy_url": "mysql+pymysql://root:password@10.5.0.5:3306/melty",
    "ssh_tunnel": {
        "enable": True,
        "host": "127.0.0.1",
        "port": 2223,
        "username": "melty",
        "private_key": "",
    },
}


def test_ssh_tunnel() -> None:
    """We expect the SSH environment to already be up."""
    # Configure paramiko logging
    paramiko.util.log_to_file("paramiko.log")
    logging.basicConfig(level=logging.DEBUG)
    paramiko_logger = logging.getLogger("paramiko")
    paramiko_logger.setLevel(logging.DEBUG)

    # Read the key *contents* from the file.  This avoids permission issues.
    key_path = Path(__file__).parent / "ssh_tunnel" / "ssh-server-config" / "ssh_host_rsa_key"
    private_key = key_path.read_text()

    SAMPLE_CONFIG["ssh_tunnel"]["private_key"] = private_key
    tap = TapMySQL(config=SAMPLE_CONFIG)
    tap.sync_all()
