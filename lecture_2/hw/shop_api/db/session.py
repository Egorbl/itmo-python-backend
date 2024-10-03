from idlelib.pyparse import trans
from typing import Annotated

from fastapi.params import Depends
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session

from lecture_2.hw.shop_api.db.models import Base


def get_connection_pool():
    engine = create_engine('postgresql+psycopg2://postgres:@localhost:5432', echo=False)
    return engine

def get_session(engine: Annotated[Engine, Depends(get_connection_pool, use_cache=True)]):
    with Session(engine) as session:
        return session

engine = create_engine('postgresql+psycopg2://postgres:@localhost:5432', echo=False)
Base.metadata.create_all(engine)