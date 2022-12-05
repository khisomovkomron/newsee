from fastapi import HTTPException
from starlette import status
from logs.loguru import fastapi_logs


logger = fastapi_logs(router='AUTH')


def get_user_exception():
    """ returns HTTP exception if users credentials are wrong"""
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Coul not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    logger.critical(credential_exception)
    return credential_exception


def token_exception():
    """returns HTTP exception if provided token by user is invalid"""
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    logger.critical(token_exception)
    return token_exception


def http_exception():
    raise HTTPException(status_code=404, detail='Not found')


def successful_response(status_code):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }
