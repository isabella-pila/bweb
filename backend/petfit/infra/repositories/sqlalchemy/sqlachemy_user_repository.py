from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from petfit.domain.entities.user import User
from petfit.domain.repositories.user_repository import UserRepository
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password
from petfit.infra.models.user_model import UserModel

from petfit.infra.database import async_session


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._current_user: Optional[UserPublic] = None # Opcional: mude para UserPublic se current_user for sem senha

    async def register(self, user: User) -> UserPublic: # <-- ALtere o tipo de retorno para UserPublic
        model = UserModel.from_entity(user)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model) # O modelo agora está atualizado com o ID do banco, etc.
        return model.to_entity() # Isso AGORA retornará um UserPublic (sem senha)

    # ... (Seu método login também precisará ser ajustado para retornar UserPublic ou User conforme seu design)
    async def login(self, email: Email, password: Password) -> Optional[UserPublic]: # Exemplo: Retorne UserPublic
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self._session.execute(stmt)
        user_model = result.scalar_one_or_none()

        if user_model and password.verify(user_model.password): # Assume que Password VO tem um método verify()
            # self._current_user = user_model.to_entity() # Se _current_user for UserPublic
            return user_model.to_entity()
        return None

    async def get_current_user(self) -> Optional[UserPublic]: # Exemplo: Retorne UserPublic
        return self._current_user

    async def set_current_user(self, user: UserPublic) -> None: # Exemplo: Aceite UserPublic
        self._current_user = user

    async def logout(self) -> None:
        self._current_user = None