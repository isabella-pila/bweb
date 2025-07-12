from petfit.domain.entities.user import User
from petfit.domain.entities.user_public import UserPublic
from petfit.domain.repositories.user_repository import UserRepository
from typing import Optional


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user: User) -> Optional[UserPublic]:
        return self.repository.register(user)
