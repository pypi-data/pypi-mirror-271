import logging
import os
import subprocess
import timeit
from pathlib import Path
from subprocess import Popen

import pexpect
from py4j.java_gateway import JavaGateway

src_dir = Path(__file__).parent / "../"
executable_name = "encryption-app.bat" if os.name == 'nt' else "encryption-app"

EXECUTABLE_PATH = src_dir / "java/encryption-app/build/distributions/encryption-app-1.0-SNAPSHOT/bin" / executable_name
logger = logging.getLogger(__name__)


def _run_command(command: str) -> Popen[bytes]:
    """Calls `command` in shell and returns its output as string.

    :param command: the command to perform.
    :return: terminal output of the command.
    """
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True)


class StringEncryptor:
    def __init__(self, algorithm: str, key: str):
        logger.info("initializing encryptor...")

        self.child = pexpect.spawn(str(EXECUTABLE_PATH))
        self.child.expect('py4j - Gateway Server Started')

        gateway = JavaGateway()
        self.encryptor = gateway.entry_point.getEncryptor()
        self.encryptor.setAlgorithm(algorithm)
        self.encryptor.setPassword(key)

    def __del__(self):
        self.child.kill(2)

    def encrypt(self, message: str):
        return self.encryptor.encrypt(message)

    def decrypt(self, message: str):
        return self.encryptor.decrypt(message)


if __name__ == '__main__':
    enc = StringEncryptor('PBEWITHSHA256AND256BITAES-CBC-BC', 'safsadfsda')

    start = timeit.default_timer()

    for _ in range(10_000):
        x = enc.encrypt("hello hasdfdsaf ello")
        dec = enc.decrypt(x)

    end = timeit.default_timer()

    print(f"{end - start:.2f}")
