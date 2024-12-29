from fastapi.responses import JSONResponse
from typing import Optional
from fastapi import HTTPException

def make_response(payload:str | dict, status:int, scope:Optional[str] = None):
    if status > 299: return JSONResponse(content={"message": payload, "status": status, "scope": scope})
    else: return JSONResponse(content={"data": payload, "status": status})

def abort(status:int, payload:str | dict):
    raise HTTPException(status_code=status, detail=payload)