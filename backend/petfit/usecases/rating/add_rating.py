from petfit.domain.entities.rating import Rating
from petfit.domain.repositories.rating_repository import RatingRepository
from typing import Optional


class AddRatingUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    def execute(self, rating: Rating) -> Optional[Rating]:
        return self.repository.add_rating(rating)