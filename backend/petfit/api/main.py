# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict # Certifique-se de que ConfigDict está importado aqui
import uuid # Para gerar IDs temporariamente

# Importações de seus domínios e use cases
from petfit.domain.entities.user import User
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password
from petfit.domain.repositories.user_repository import UserRepository # Sua interface abstrata de repositório

# Importações das implementações do repositório (para injeção de dependência)
from petfit.infra.repositories.in_memory.in_memory_user_repository import InMemoryUserRepository

# Importações dos seus Use Cases (cuidado com o nome do arquivo update.user.py)
from petfit.usecases.user.register_user import RegisterUserUseCase
from petfit.usecases.user.login_user import LoginUserUseCase
from petfit.usecases.user.logout_user import LogoutUserUseCase
from petfit.usecases.user.get_current_user import GetCurrentUserUseCase
from petfit.usecases.user.set_current_user import SetCurrentUserUseCase
# Ajuste conforme o nome real do seu arquivo, ex: update_user.py
from petfit.usecases.user.update_user import UpdateUserUseCase # Assumindo que o arquivo é 'update.py' dentro de user/

app = FastAPI(
    title="Petfit API",
    description="API para gerenciamento de perfis de pets, receitas e avaliações.",
    version="0.0.1",
)

# --- Dependências (Injeção de Repositório) ---
def get_user_repository() -> UserRepository:
    # Retorna uma instância do repositório em memória para demonstração/desenvolvimento
    return InMemoryUserRepository()

# --- Modelos Pydantic para Requisição e Resposta (Input/Output da API) ---
# A propriedade 'model_config' é para Pydantic v2.x
# Ela permite que Pydantic trabalhe com tipos customizados como seus VOs.

class UserBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True) # ADICIONADO/MANTIDO
    name: str
    email: Email # Usando seu VO Email
    password: Password # Usando seu VO Password

class UserRegisterRequest(UserBase):
    pass # Pode adicionar campos específicos para registro se houver

class UserLoginRequest(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True) # ADICIONADO/MANTIDO
    email: Email # Usando seu VO Email
    password: Password # Usando seu VO Password

class UserResponse(UserBase):
    model_config = ConfigDict(arbitrary_types_allowed=True) # ADICIONADO/MANTIDO
    id: str # ID é gerado, então aparece na resposta
    # CUIDADO: NUNCA retorne a senha real em uma resposta de API em produção.
    # Esta linha é apenas para que o esquema Pydantic saiba que o campo existe.
    password: str = "******" # Substitui a senha real por asteriscos para a documentação

# Endpoint de teste simples para verificar se a API está rodando
@app.get("/")
async def read_root():
    return {"message": "API is running!"}


# --- Rotas para Usuários ---

@app.post("/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user_route( # Renomeado para evitar conflito com RegisterUserUseCase
    user_data: UserRegisterRequest,
    repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    """
    Registra um novo usuário no sistema.
    """
    new_user = User(
        id=str(uuid.uuid4()), # Gerar ID aqui ou no use case/repositório
        name=user_data.name,
        email=user_data.email, # Já é um VO Email aqui
        password=user_data.password, # Já é um VO Password aqui
    )
    
    usecase = RegisterUserUseCase(repo)
    registered_user = usecase.execute(new_user)

    if not registered_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User registration failed. Email might already exist."
        )
    return registered_user

@app.post("/users/login", response_model=UserResponse)
async def login_user_route( # Renomeado para evitar conflito
    credentials: UserLoginRequest,
    repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    """
    Autentica um usuário e retorna seus dados.
    """
    usecase = LoginUserUseCase(repo)
    logged_in_user = usecase.execute(credentials.email, credentials.password)

    if not logged_in_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )
    return logged_in_user

@app.post("/users/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user_route( # Renomeado para evitar conflito
    repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    """
    Desconecta o usuário atual.
    """
    usecase = LogoutUserUseCase(repo)
    usecase.execute()
    # Não há retorno de conteúdo para 204 No Content

@app.get("/users/current", response_model=Optional[UserResponse])
async def get_current_user_route( # Renomeado para evitar conflito
    repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    """
    Retorna os dados do usuário atualmente logado (se houver).
    """
    usecase = GetCurrentUserUseCase(repo)
    current_user = usecase.execute()
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user is currently logged in."
        )
    return current_user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user_route( # Renomeado para evitar conflito
    user_id: str,
    user_data: UserRegisterRequest, # Pode ser um UserUpdateRequest com campos opcionais
    repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    """
    Atualiza os dados de um usuário existente.
    """
    # Primeiro, obter o usuário existente para não perder dados
    existing_user = repo.get_by_id(user_id) # Usando o método que você adicionou
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # Criar um objeto User com os dados atualizados
    updated_user_entity = User(
        id=user_id,
        name=user_data.name if user_data.name else existing_user.name,
        email=user_data.email if user_data.email else existing_user.email,
        password=user_data.password if user_data.password else existing_user.password,
    )

    usecase = UpdateUserUseCase(repo)
    updated_result = usecase.execute(updated_user_entity)

    if not updated_result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, # Ou 400 Bad Request
            detail="Failed to update user."
        )
    return updated_result