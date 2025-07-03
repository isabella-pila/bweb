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
        self._current_user: Optional[User] = None

    async def register(self, user: User) -> User:
        model = UserModel.from_entity(user)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model.to_entity()

    async def login(self, email: Email, password: Password) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()

        if user and user.password == password.verify(user.password):
            self._current_user = user.to_entity()
            return self._current_user
        return None

    async def get_current_user(self) -> Optional[User]:
        return self._current_user

    async def set_current_user(self, user: User) -> None:
        self._current_user = user

    async def logout(self) -> None:
        self._current_user = None