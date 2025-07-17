# petfit/api/deps.py

# Instâncias SQLAlchemy
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from petfit.api.settings import settings
from petfit.domain.repositories.user_repository import UserRepository
from petfit.infra.repositories.sqlalchemy.sqlachemy_user_repository import (
    SQLAlchemyUserRepository,
)
from petfit.infra.repositories.sqlalchemy.sqlalchemy_recipe_repository import (
    SQLAlchemyRecipeRepository, # <-- Certifique-se que esta importação está aqui
)

from sqlalchemy.ext.asyncio import AsyncSession
from petfit.infra.database import async_session
from petfit.domain.entities.user import User
from collections.abc import AsyncGenerator


# Dependência para obter a sessão do banco de dados
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# Dependência para obter a instância do repositório de usuários
async def get_user_repository(
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)


# Dependência para obter a instância do repositório de receitas
async def get_recipe_repository( # <-- NOVA DEPENDÊNCIA ADICIONADA AQUI
    db: AsyncSession = Depends(get_db_session),
) -> SQLAlchemyRecipeRepository:
    return SQLAlchemyRecipeRepository(db)


# Esquema OAuth2 para extrair o token do cabeçalho de autorização
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# Dependência para obter o usuário atualmente autenticado
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token JWT
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        # Extrai o ID do usuário (sub) do payload
        user_id: str = str(payload.get("sub"))
        if not user_id:
            raise credentials_exception

        # Busca o usuário no banco de dados usando o ID do token
        user = await user_repo.get_by_id(user_id)
        if user is None:
            # Se o usuário não existe no DB, as credenciais ainda são inválidas
            raise credentials_exception
        
        # Retorna o objeto User encontrado
        return user 

    except JWTError:
        # Lida com erros de token JWT (expirado, inválido, etc.)
        raise credentials_exception
    except Exception as e:
        # Captura qualquer outro erro inesperado e loga para depuração
        print(f"Erro inesperado em get_current_user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during authentication."
        )