from fastapi import HTTPException, Depends
from starlette import status
from logs.loguru import fastapi_logs

logger = fastapi_logs(router='AUTH')


def get_user_exception(exception: Depends(HTTPException)):
    """ returns HTTP exception if users credentials are wrong"""
    credential_exception = exception(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    logger.critical(credential_exception)
    return credential_exception


def user_exception(exception: Depends(HTTPException)):
    raise exception(status_code=400, detail="User already exists")


def token_exception(exception: Depends(HTTPException)):
    """returns HTTP exception if provided token by user is invalid"""
    token_exception = exception(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    logger.critical(token_exception)
    return token_exception


def http_exception(exception: Depends(HTTPException), status_code: int, detail: str):
    raise exception(status_code=404, detail=detail)


def successful_response(status_code):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }

