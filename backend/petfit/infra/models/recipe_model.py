from sqlalchemy import Column, String, Text, DateTime
from petfit.infra.database import Base
from datetime import datetime


class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    ingredients = Column(String, nullable=False)
    instructions = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
    category = Column(String, nullable=False)
