from petfit.domain.entities.user import User
from petfit.domain.entities.user_public import UserPublic
from petfit.domain.repositories.user_repository import UserRepository
from typing import Optional

class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_entity: User) -> Optional[UserPublic]:

        registered_user_model = await self.repository.register(user_entity)

        if registered_user_model:
            return registered_user_model.to_entity()
        return None