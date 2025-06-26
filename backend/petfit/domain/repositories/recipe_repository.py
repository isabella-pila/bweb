from abc import ABC, abstractmethod
from petfit.domain.entities.recipe import Recipe


class RecipeRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[Recipe]:
        pass

    @abstractmethod
    def get_by_id(self, recipe_id: str) -> Recipe:
        pass

    @abstractmethod
    def create(self, recipe: Recipe) -> None:
        pass

    @abstractmethod
    def delete(self, recipe_id: str) -> None:
        pass







