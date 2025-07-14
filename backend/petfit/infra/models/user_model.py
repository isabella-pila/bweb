from sqlalchemy import String, Column
from petfit.infra.database import Base
from petfit.domain.entities.user import User # Para from_entity
from petfit.domain.entities.user_public import UserPublic # Para to_entity
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 

    @classmethod
    def from_entity(cls, user_entity: User):
        """Converte uma entidade User para um modelo UserModel."""
        return cls(
            id=user_entity.id,
            name=user_entity.name,
            email=str(user_entity.email),
            password=str(user_entity.password.value()) 
        )

    def to_entity(self) -> UserPublic: 
        """Converte um modelo UserModel para uma entidade UserPublic."""
       
        return UserPublic(
            id=self.id,
            name=self.name,
            email=Email(self.email) #
        )