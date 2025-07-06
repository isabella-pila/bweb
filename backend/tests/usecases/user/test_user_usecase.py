import uuid
from petfit.domain.entities.user import User
from petfit.domain.value_objects.email_vo import Email
from petfit.domain.value_objects.password import Password
from petfit.infra.repositories.in_memory.in_memory_user_repository import InMemoryUserRepository
from petfit.usecases.user.register_user import RegisterUserUseCase
from petfit.usecases.user.login_user import LoginUserUseCase
from petfit.usecases.user.logout_user import LogoutUserUseCase
from petfit.usecases.user.get_current_user import GetCurrentUserUseCase
from petfit.usecases.user.set_current_user import SetCurrentUserUseCase
from petfit.usecases.user.update_user import UpdateUserUseCase


def create_test_user() -> User:
    return User(
        id=str(uuid.uuid4()),
        name="Test User",
        email=Email("test@example.com"),
        password=Password("secur3@Pass"),
    )


def test_register_user():
    repo = InMemoryUserRepository()
    usecase = RegisterUserUseCase(repo)
    user = create_test_user()

    result = usecase.execute(user)

    assert result == user
    assert repo.get_current_user() == user


def test_login_user_success():
    repo = InMemoryUserRepository()
    user = create_test_user()
    repo.register(user)

    usecase = LoginUserUseCase(repo)
    result = usecase.execute(user.email, user.password)

    assert result == user
    assert repo.get_current_user() == user


def test_login_user_failure():
    repo = InMemoryUserRepository()
    usecase = LoginUserUseCase(repo)
    email = Email("notfound@example.com")
    password = Password("wrongP@1ss")

    result = usecase.execute(email, password)

    assert result is None
    assert repo.get_current_user() is None


def test_logout_user():
    repo = InMemoryUserRepository()
    user = create_test_user()
    repo.register(user)
    repo.login(user.email, user.password)

    usecase = LogoutUserUseCase(repo)
    usecase.execute()

    assert repo.get_current_user() is None


def test_get_current_user():
    repo = InMemoryUserRepository()
    user = create_test_user()
    repo.register(user)

    usecase = GetCurrentUserUseCase(repo)
    result = usecase.execute()

    assert result == user


def test_set_current_user():
    repo = InMemoryUserRepository()
    user = create_test_user()

    usecase = SetCurrentUserUseCase(repo)
    usecase.execute(user)

    assert repo.get_current_user() == user

def test_update_user():
    repo = InMemoryUserRepository()
    user = create_test_user()
    repo.register(user)  # usar register, não create

    email = Email("user@example.com")
    password = Password("Secret123!")

    updated = User(
        id=user.id,
        name="pila",
        email=user.email,       # <--- Adicionado
        password=user.password         # <--- Adicionado (se 'role' for obrigatório)
    )

    usecase = UpdateUserUseCase(repo)
    result = usecase.execute(updated)

    assert result.name == "pila"
    assert repo.get_by_id(user.id).name == "pila"


def test_update_user_not_found():
    repo = InMemoryUserRepository()
    user = create_test_user()

    usecase = UpdateUserUseCase(repo)
    result = usecase.execute(user)

    assert result is None



