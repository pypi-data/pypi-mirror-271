from fastapi import APIRouter
from starlette.responses import HTMLResponse

from .measure_service import profiling_service

#
# @author: andy
#
profiler_router = APIRouter()


@profiler_router.get("/profiler", response_class=HTMLResponse)
def index():
    return HTMLResponse(content=profiling_service.as_html(), status_code=200)
