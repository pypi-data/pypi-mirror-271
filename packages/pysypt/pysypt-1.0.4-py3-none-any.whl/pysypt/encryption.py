import logging
import os
from pathlib import Path

import pexpect
from py4j.java_gateway import JavaGateway

logger = logging.getLogger(__name__)

src_dir = Path(__file__).parent / "../"
executable_name = "encryption-app.bat" if os.name == 'nt' else "encryption-app"

EXECUTABLE_PATH = src_dir / "java/encryption-app/build/distributions/encryption-app-1.0-SNAPSHOT/bin" / executable_name


class JavaAppServer:
    """Launches and connects to the py4j app
    """

    def __init__(self):
        self.child = pexpect.spawn(str(EXECUTABLE_PATH))
        self.child.expect('py4j - Gateway Server Started')

        gateway = JavaGateway()
        self.encryptor = gateway.entry_point.getEncryptor()

    def __del__(self):
        self.child.kill(2)


JAVA_APP = JavaAppServer()


class StringEncryptor:
    def __init__(self, algorithm: str, key: str):
        self.encryptor = JAVA_APP.encryptor
        self.encryptor.setAlgorithm(algorithm)
        self.encryptor.setPassword(key)

    def encrypt(self, message: str):
        return self.encryptor.encrypt(message)

    def decrypt(self, message: str):
        return self.encryptor.decrypt(message)
