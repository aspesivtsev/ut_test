from fastapi import Depends, APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlmodel import Session
from starlette import status

import logging
from ..db import get_session
from ..schemas import Movies
from ..lib import clean_number

logging.basicConfig(filename='api_log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

# задаем необходимый префикс
router = APIRouter(prefix="/api/v1")


@router.get("/get_all_data/")
def get_all_data(session: Session = Depends(get_session)) -> JSONResponse:
    """Метод предоставляет выгрузку всех объектов из таблицы movies"""
    all_movies = session.query(Movies).all()
    if not all_movies:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return all_movies
