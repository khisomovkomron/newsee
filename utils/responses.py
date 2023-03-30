from fastapi import HTTPException, status


class CustomResponse(HTTPException):
    """Исключение доменной логики"""

    status: int
    message: str


class Success(CustomResponse):
    """Successful response"""

    status = status.HTTP_200_OK
    message = 'OK'


class Created(CustomResponse):

    status = status.HTTP_201_CREATED
    message = 'CREATED'