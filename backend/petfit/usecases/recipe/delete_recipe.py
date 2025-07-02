from petfit.domain.repositories.recipe_repository import RecipeRepository


class DeleteRecipeUseCase:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository

    def execute(self, recipe_id: str) -> bool:
        self.repository.delete(recipe_id)
        return True