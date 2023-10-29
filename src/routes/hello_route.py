from fastapi import APIRouter

from src.common.response import Response

router = APIRouter()


@router.get("/hello")
def get_hello():
    return Response(
        code=200,
        status="Ok",
        result="Hello!"
    ).dict(exclude_none=True)
