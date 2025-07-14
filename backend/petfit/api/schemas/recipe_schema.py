from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime
from petfit.domain.entities.recipe import Recipe


class RecipeCreateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título da Receita")
    instructions: str = Field(
        ..., min_length=10, max_length=300, description="Descrição da receita"
    )
    ingredients: str = Field(..., min_length=20, description="Conteúdo da receita")
    


class RecipeUpdateInput(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, description="Título da receita")
    instructions: str = Field(
        ..., min_length=10, max_length=300, description="Descrição da receita"
    )
    ingredients: str = Field(..., min_length=20, description="Conteúdo da receita")


class RecipeOutput(BaseModel):
    id: str = Field(..., description="ID da receita")
    title: str = Field(..., min_length=3, max_length=100, description="Título da receita")
    instructions: str = Field(
        ..., min_length=10, max_length=300, description="Descrição da receita"
    )
    ingredients: str = Field(..., min_length=20, description="Conteúdo da receita")
    

    @classmethod
    def from_entity(cls, recipe):
        return cls(
            id=recipe.id,
            title=recipe.title,
            instructions=recipe.instructions,
            ingredients=recipe.ingredients,
        )



def recipe_to_output(recipe: Recipe) -> RecipeOutput:
        return RecipeOutput(
        id=recipe.id,
        title=recipe.title,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        
    )


def recipes_to_output(recipes: list[Recipe]) -> list[RecipeOutput]:
        return [recipe_to_output(recipe) for recipe in recipes] 