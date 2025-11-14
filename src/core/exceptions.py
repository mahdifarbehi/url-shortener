from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, cls_name: str = "Object"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{cls_name} not found",
        )


class BadRequestException(HTTPException):
    def __init__(self, detail="Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
