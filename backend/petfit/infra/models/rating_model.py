from sqlalchemy import Column, String, Text, ForeignKey
from petfit.infra.database import Base


class PostModel(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    value = Column(int, nullable=True)
    recipes_id = Column(String, ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)