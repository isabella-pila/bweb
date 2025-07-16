from fastapi import APIRouter, HTTPException, Depends, status # Importe status para usar HTTP_201_CREATED
from petfit.usecases.user.register_user import RegisterUserUseCase
from petfit.usecases.user.login_user import LoginUserUseCase
from petfit.usecases.user.logout_user import LogoutUserUseCase
from petfit.usecases.user.get_current_user import GetCurrentUserUseCase
from petfit.domain.entities.user import User
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password, PasswordValidationError
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from petfit.api.deps import get_db_session, get_user_repository, get_current_user
from petfit.infra.repositories.sqlalchemy.sqlachemy_user_repository import (
    SQLAlchemyUserRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from petfit.api.schemas.user_schema import (
    RegisterUserInput,
    UserOutput,
    TokenResponse,
)
from petfit.api.schemas.message_schema import MessageOutput
from petfit.api.security import create_access_token
from petfit.domain.repositories.user_repository import UserRepository
from petfit.api.schemas.user_schema import LoginUserInput
from petfit.api.security import verify_token

security = HTTPBearer()
router = APIRouter()

# ----------------------
# Register
# ----------------------


@router.post(
    "/register",
    response_model=MessageOutput,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, email e senha forte.",
    status_code=status.HTTP_201_CREATED # Boa prática para criação
)
async def register_user(
    data: RegisterUserInput, db: AsyncSession = Depends(get_db_session)
):
    try:
        user_repo = SQLAlchemyUserRepository(db)
        usecase = RegisterUserUseCase(user_repo)
        user = User(
            id=str(uuid.uuid4()),
            name=data.name,
            email=Email(data.email),
            password=data.password, # <--- CORRIGIDO: Use o objeto Password já validado pelo Pydantic
        )
        await usecase.execute(user)
        return MessageOutput(
            message="User registered successfully"
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        # Captura outros ValueErrors, como "User with this email already exists"
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Um catch-all para erros inesperados
        print(f"Erro inesperado no registro: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# ----------------------
# Login
# ----------------------


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Fazer o Login do usuário",
    description="Autentica um usuário com email e senha forte.",
)
async def login_user(
    data: LoginUserInput,
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = LoginUserUseCase(user_repo)
        # O Pydantic já validou data.password para ser um Password object.
        # Mas para a verificação de login, você precisa da senha em texto CLARO
        # para que o bcrypt.checkpw possa funcionar.
        #
        # O data.password agora é um objeto Password *com o hash dentro*.
        # Você PRECISA do valor em texto CLARO que veio na requisição para verificar.
        #
        # Solução: Use o `data.password` original da Pydantic request body,
        # MAS seu LoginUserUseCase e Password.verify precisam ser ajustados
        # para usar o valor em texto claro da entrada.

        # *** REVISÃO CRÍTICA AQUI ***
        # Se LoginUserInput.password é `Password`, o Pydantic vai hashá-la *antes* de chegar aqui.
        # Isso não é o que você quer para login, você quer a senha em texto claro.
        #
        # Em LoginUserInput, a `password` DEVE ser `str`, e você vai hasheá-la (ou verificá-la) *manualmente*.
        #
        # Então, o `LoginUserInput` deveria ser assim:
        # class LoginUserInput(BaseModel):
        #     email: EmailStr
        #     password: str # <--- STRING AQUI PARA LOGIN!

        # Com a modificação acima, o código de login ficaria assim:
        # user = await usecase.execute(Email(data.email), data.password) # Passa a string
        # e o LoginUserUseCase vai chamar Password.verify(data.password) com a string

        # Se você insistir em data.password ser um objeto Password com o hash,
        # então seu LoginUserUseCase ou Password.verify precisarão de uma forma
        # de acessar a senha original do input, o que é contraproducente.

        # Assumindo que `LoginUserInput.password` foi alterado para `str`:
        user = await usecase.execute(Email(data.email), data.password) # data.password é a string em texto claro

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(data={"sub": user.id})
        return TokenResponse(
            access_token=token, token_type="bearer", user=UserOutput.from_entity(user)
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e: # Pode ser "Invalid credentials" ou "User not found"
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        print(f"Erro inesperado no login: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


# ----------------------
# Get Current User
# ----------------------


@router.get(
    "/me",
    response_model=UserOutput,
    summary="Informar os dados do usuário atual",
    description="Retorna os dados do usuário atual.",
)
async def get_me_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
):
    try:
        # Se 'user' já é uma entidade User, você pode retorná-la diretamente
        # ou usar UserOutput.from_entity(user)
        return UserOutput.from_entity(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        print(f"Erro inesperado ao obter usuário atual: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")