from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

# Importações de suas camadas de domínio e infraestrutura
from petfit.domain.entities.user import User # Para a entidade de input/processamento
from petfit.domain.entities.user_public import UserPublic # Para a entidade de output/resposta
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password, PasswordValidationError
from petfit.domain.repositories.user_repository import UserRepository

# Importações de casos de uso (usecases)
from petfit.usecases.user.register_user import RegisterUserUseCase
from petfit.usecases.user.login_user import LoginUserUseCase
from petfit.usecases.user.logout_user import LogoutUserUseCase
from petfit.usecases.user.get_current_user import GetCurrentUserUseCase

# Importações de dependências e repositórios (infraestrutura)
from petfit.api.deps import get_db_session, get_user_repository, get_current_user
from petfit.infra.repositories.sqlalchemy.sqlachemy_user_repository import (
    SQLAlchemyUserRepository,
)

# Importações de schemas Pydantic para requisição e resposta
from petfit.api.schemas.user_schema import (
    RegisterUserInput,
    UserOutput,
    MessageUserResponse,
    LoginUserInput, # Adicionado, embora não usado diretamente aqui, é comum ter
)
from petfit.api.schemas.token_schema import TokenResponse
from petfit.api.security import create_access_token


router = APIRouter()

# ----------------------
# Register
# ----------------------

@router.post(
    "/register",
    response_model=MessageUserResponse,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com nome, email e senha forte.",
)
async def register_user_route( # Renomeado para evitar possível conflito com nome de usecase
    data: RegisterUserInput, db: AsyncSession = Depends(get_db_session)
):
    try:
        user_repo = SQLAlchemyUserRepository(db)
        usecase = RegisterUserUseCase(user_repo)

        # Cria a entidade de domínio User para passar para o usecase
        user_entity_for_creation = User(
            id=str(uuid.uuid4()), # Geração de UUID aqui para a entidade de domínio
            name=data.name,
            email=Email(data.email),
            password=Password(data.password),
        )

        # Executa o usecase, que agora retorna um UserPublic
        registered_user_public: UserPublic = await usecase.execute(user_entity_for_creation)

        if not registered_user_public:
            # Isso pode acontecer se, por exemplo, o registro falhar no usecase
            raise HTTPException(status_code=500, detail="Failed to register user")

        return MessageUserResponse(
            message="User registered successfully",
            user=UserOutput.from_entity(registered_user_public) # Converte UserPublic para UserOutput
        )
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: # Captura erros gerais para depuração
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# ----------------------
# Login
# ----------------------

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Fazer o Login do usuário",
    description="Autentica um usuário com email e senha forte.",
)
async def login_user_route( # Renomeado para evitar possível conflito
    data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = LoginUserUseCase(user_repo)
        # O LoginUserUseCase deve retornar o UserPublic ou uma entidade que tenha o ID para o token
        user = await usecase.execute(Email(data.username), Password(data.password)) # OAuth2PasswordRequestForm usa 'username' para o primeiro campo
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # 'user' aqui deve ser o UserPublic ou ter um atributo 'id'
        token = create_access_token(data={"sub": user.id}) 
        return TokenResponse(access_token=token, token_type="bearer")
    except PasswordValidationError as p:
        raise HTTPException(status_code=400, detail=str(p))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# ----------------------
# Logout
# ----------------------

@router.post(
    "/logout",
    summary="Fazer o Logout do usuário",
    description="Descredencia o usuário autenticado.",
)
async def logout_user_route( # Renomeado
    user: User = Depends(get_current_user), # A dependência get_current_user injeta a entidade User
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = LogoutUserUseCase(user_repo)
        await usecase.execute(user.id)
        return {"message": "Logout successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# ----------------------
# Get Current User
# ----------------------

@router.get(
    "/me",
    response_model=UserOutput,
    summary="Informar os dados do usuário atual",
    description="Retorna os dados do usuário atual.",
)
async def get_current_user_route_handler( # Renomeado para evitar conflito com a dependência
    # A dependência get_current_user injeta a entidade User
    current_user_entity: User = Depends(get_current_user), 
    user_repo: UserRepository = Depends(get_user_repository),
):
    try:
        usecase = GetCurrentUserUseCase(user_repo)
        
        # O usecase agora espera o ID do usuário e retorna UserPublic
        user_public_data: UserPublic = await usecase.execute(current_user_entity.id)

        if not user_public_data:
            raise HTTPException(status_code=404, detail="User not found")

        # Converte a entidade UserPublic para o schema UserOutput para a resposta
        return UserOutput.from_entity(user_public_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")