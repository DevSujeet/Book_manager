import time
from fastapi import HTTPException, Header, Request
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from src.config.configs import _ctx_var
from src.exceptions.exception import SourceException
from src.schemas.system_message import SystemMessage
from fastapi.encoders import jsonable_encoder

class ErrorTemplate:
    pass

async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time"] = str(process_time)
    return response

async def source_exception_handler(request: Request, ex: SourceException):
    return JSONResponse(
        status_code=ex.code,
        content=jsonable_encoder(SystemMessage(code=ex.code, message=ex.message, displayMessage=ex.displayMessage)),
    )
