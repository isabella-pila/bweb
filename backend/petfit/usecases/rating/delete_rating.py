from petfit.domain.repositories.rating_repository import RatingRepository


class DeleteRatingUseCase:
    def __init__(self, repository: RatingRepository):
        self.repository = repository

    def execute(self, rating_id: str) -> bool:
        self.repository.delete_rating(rating_id)
        return True