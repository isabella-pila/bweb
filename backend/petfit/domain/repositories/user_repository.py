from abc import ABC, abstractmethod
from petfit.domain.entities.user import User
from typing import Optional

class UserRepository(ABC):
    @abstractmethod
    def login(self,email:str,password:str) -> User:
        pass

    @abstractmethod
    def register(self, user: User) -> None:
        pass

    @abstractmethod
    def get_current_user(self) -> Optional[User]: # pode ser user ou pode ser que venha none
        pass

    @abstractmethod
    def set_current_user(self,user:User) -> None:
        pass

    @abstractmethod
    def user_logout(self) -> None:
        pass
