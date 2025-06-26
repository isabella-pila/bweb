from abc import ABC, abstractmethod
from petfit.domain.entities.recipe import Recipe
from petfit.domain.entities.rating import Rating

class RecipeRepository(ABC):
    @abstractmethod
    def get_rating_by_recipe(self, recipe_id: str) -> list[Recipe]:
        pass

    @abstractmethod
    def get_rating_by_user(self, user_id: str) -> list[Recipe]:
        pass

    @abstractmethod
    def add_rating(self, rating: Rating) -> None:
        pass

    @abstractmethod
    def update(self, rating: Rating) -> None:
        pass
