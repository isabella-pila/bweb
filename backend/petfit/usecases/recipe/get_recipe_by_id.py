from petfit.domain.repositories.recipe_repository import RecipeRepository
from petfit.domain.entities.recipe import Recipe
from typing import Optional


class GetRecipeByIdUseCase:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    def execute(self, recipe_id: str) -> Optional[Recipe]:
        return self.repository.get_by_id(recipe_id)