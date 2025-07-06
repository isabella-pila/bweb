from pydantic import BaseModel, Field, ConfigDict, conint
from typing import Optional
from datetime import datetime



class Avaliacao(BaseModel):
    rating: conint(ge=1, le=5, description="Avaliação entre 1 e 5")



class AddRatingInput(BaseModel):
    recipe_id: str = Field(
        ..., description="ID da receita ao qual a avaliação será adicionado"
    )
    rating: conint(ge=1, le=5, description="Avaliação entre 1 e 5")
    date: datetime = Field(..., description="Data da avaliação no formato ISO 8601")


class RatingOutput(BaseModel):
    id: str = Field(..., description="ID da avaliação")
    recipe_id: str = Field(..., description="ID do receita ao qual a avaliação pertence")
    user_id: str = Field(..., description="ID do usuário que fez a avaliação")
    rating: conint(ge=1, le=5, description="Avaliação entre 1 e 5")
    date: datetime = Field(..., description="Data da avaliação no formato ISO 8601")

    @classmethod
    def from_entity(cls, rating):
        return cls(
            id=rating.id,
            recipe_id=rating.recipe_id,
            user_id=rating.user_id,
            rating=rating.rating,
            date=rating.date,
        )