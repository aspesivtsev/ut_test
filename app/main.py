from fastapi import FastAPI, Request

import logging
import uvicorn

#from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from .db import engine
from .routers import tu

from sqlmodel import SQLModel
from starlette.responses import JSONResponse

from contextlib import asynccontextmanager
#from routers.cars import BadTripException

# эквивалент метода @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load something before startup
    SQLModel.metadata.create_all(engine)
    yield
    # do something just before the closing application

app = FastAPI(lifespan=lifespan, title="API for UT")
app.include_router(tu.router)

logger = logging.getLogger(__name__)
