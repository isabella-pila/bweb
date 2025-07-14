from petfit.domain.repositories.user_repository import UserRepository
from petfit.domain.entities.user import User # Mantenha a importação se o repositório retornar User
from petfit.domain.entities.user_public import UserPublic # Importe UserPublic
from typing import Optional

class GetCurrentUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: str) -> Optional[UserPublic]: 
    
        user_model = await self.repository.get_user_by_id(user_id) 

        if user_model:
            return user_model.to_entity()
        return None