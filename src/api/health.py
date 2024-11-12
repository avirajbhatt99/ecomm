from fastapi import status, APIRouter
from fastapi.responses import JSONResponse


health_router = APIRouter(prefix="/v1")


@health_router.get("/health")
def health_check():
    """
    Endpoint to check health of the server
    """
    return JSONResponse(status_code=status.HTTP_200_OK)
