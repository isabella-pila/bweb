from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime


class RecipeCreateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título da Receita")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição da receita"
    )
    content: str = Field(..., min_length=20, description="Conteúdo da receita")
    date: datetime = Field(..., description="Data de criação da receita")


class RecipeUpdateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título da receita")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição da receita"
    )
    content: str = Field(..., min_length=20, description="Conteúdo da receita")


class receitaOutput(BaseModel):
    id: str = Field(..., description="ID da receita")
    title: str = Field(..., min_length=3, max_length=100, description="Título da receita")
    description: str = Field(
        ..., min_length=10, max_length=300, description="Descrição da receita"
    )
    content: str = Field(..., min_length=20, description="Conteúdo da receita")
    date: datetime = Field(..., description="Data de criação da receita")

    @classmethod
    def from_entity(cls, recipe):
        return cls(
            id=recipe.id,
            title=recipe.title,
            instructions=recipe.instructions,
            ingredients=recipe.ingredients,
        )