import logging

from src.pysypt import JAVA_APP

logger = logging.getLogger(__name__)


class StringEncryptor:
    def __init__(self, algorithm: str, key: str):
        logger.info("initializing encryptor...")

        self.encryptor = JAVA_APP.encryptor
        self.encryptor.setAlgorithm(algorithm)
        self.encryptor.setPassword(key)

    def encrypt(self, message: str):
        return self.encryptor.encrypt(message)

    def decrypt(self, message: str):
        return self.encryptor.decrypt(message)
