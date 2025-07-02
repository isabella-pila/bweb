from petfit.domain.repositories.recipe_repository import RecipeRepository
from petfit.domain.entities.recipe import Recipe
from typing import List


class GetAllRecipesUseCase:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    def execute(self) -> List[Recipe]:
        return self.repository.get_all()