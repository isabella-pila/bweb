import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from petfit.domain.entities.recipe import Recipe
import uuid
from sqlalchemy import Column, String, Text, DateTime
from petfit.infra.database import Base
from datetime import datetime
from petfit.infra.models.user_model import UserModel

class RecipeModel(Base):
    __tablename__ = "recipes"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    title: Mapped[str] = mapped_column(sa.String(100), nullable=False) # Mantido String(100)
    ingredients: Mapped[str] = mapped_column(sa.String, nullable=False)
    instructions: Mapped[str] = mapped_column(sa.String, nullable=False)
    img_url: Mapped[str] = mapped_column(sa.String, nullable=False)
    category: Mapped[str] = mapped_column(sa.String, nullable=False)

    @classmethod
    def from_entity(cls, entity: Recipe) -> "RecipeModel":
        return cls(
            id=entity.id,
            title=entity.title,
            ingredients=entity.ingredients,
            instructions=entity.instructions,
            category=entity.category,
            img_url=entity.img_url,
        )

    def to_entity(self) -> Recipe:
        return Recipe(
            id=self.id,
            title=self.title,
            ingredients=self.ingredients,
            instructions=self.instructions,
            category=self.category,
            img_url=self.img_url
        )