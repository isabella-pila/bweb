from petfit.domain.entities.recipe import Recipe
from petfit.domain.repositories.recipe_repository import RecipeRepository
from typing import Optional


class CreateRecipeUseCase:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    def execute(self, recipe: Recipe) -> Optional[Recipe]:
        return self.repository.create(recipe)