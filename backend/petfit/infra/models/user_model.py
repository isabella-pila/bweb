import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from petfit.domain.entities.user import User
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password
import uuid
from petfit.infra.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        sa.String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    email: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    
    @classmethod
    def from_entity(cls, entity: User) -> "UserModel":
        return cls(
            id=entity.id,
            name=entity.name,
            email=str(entity.email),
            password=str(entity.password),
            
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=Email(self.email),
            password=Password(self.password),
            
        )