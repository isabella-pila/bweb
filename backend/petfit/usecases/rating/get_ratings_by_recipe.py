from petfit.domain.repositories.rating_repository import RatingRepository
from petfit.domain.entities.rating import Rating
from typing import List


class GetRatingsByRecipeUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    def execute(self, recipe_id: str) -> List[Rating]:
        return self.repository.get_ratings_by_recipe(recipe_id)
    


    