import os

from loguru import logger


def fastapi_logs(router: str):

    logger.add(f'./logs/LOGS/{router}.log', colorize=True, format="<blue>{time}</blue>: <level>{message}</level>", level='INFO', rotation="5 MB")
    return logger
    