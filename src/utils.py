import os


def get_env_variable(name) -> str:
    return os.getenv(name)

