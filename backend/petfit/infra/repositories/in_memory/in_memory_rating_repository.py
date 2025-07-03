from petfit.domain.repositories.rating_repository import RatingRepository
from petfit.domain.entities.rating import Rating
from typing import List, Optional


class InMemoryCommentRepository(RatingRepository):
    def __init__(self):
        self._ratings = {}

    def get_ratings_by_recipes(self, recipe_id: str) -> List[Rating]:
        return [c for c in self._ratings.values() if c.recipe_id == recipe_id]

    def get_ratings_by_user(self, user_id: str) -> List[Rating]:
        return [c for c in self._ratings.values() if c.user_id == user_id]

    def add_rating(self, rating: Rating) -> Rating:
        self._ratings[rating.id] = rating
        return rating

    def delete_rating(self, rating_id: str) -> None:
        self._ratings.pop(rating_id, None)