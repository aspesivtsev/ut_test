from sqlmodel import SQLModel, Field


class Movies(SQLModel, table=True):
    movie_id: str | None = Field(default=None, primary_key=True)
    name: str
    oscar: int 




# from sqlalchemy import Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Movie(Base):
#     __tablename__ = "movies",
#     __table_args__ = {"schema": "dwh_ods"}  

#     movie_id = Column(String, primary_key=True, index=True)
#     name = Column(String)
#     oscar = Column(Integer)
