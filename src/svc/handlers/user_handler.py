import hashlib

from core.config import config


def hash_password(password: str) -> str:
    hash_password = hashlib.md5(f"{password}{config.SALT}".encode()).hexdigest()
    return hash_password


def validate_pass(db_password, password: str) -> bool:
    hash_password = hashlib.md5(f"{password}{config.SALT}".encode()).hexdigest()
    return db_password == hash_password
