from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class RegisterUserInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nome do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")


class LoginUserInput(BaseModel):
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, description="Senha do usuário")


class SetCurrentUserInput(BaseModel):
    user_id: str = Field(..., description="ID do usuário a ser definido como atual")


class UserOutput(BaseModel):
    id: str = Field(..., description="ID do usuário")
    name: str = Field(..., min_length=3, max_length=50, description="Nome do usuário")
    email: str = Field(..., description="Email do usuário")
    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            name=user.name,
            email=str(user.email),
        )


class MessageUserResponse(BaseModel):
    message: str
    user: UserOutput