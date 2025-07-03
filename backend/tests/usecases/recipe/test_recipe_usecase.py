import uuid
from petfit.domain.entities.recipe import Recipe
from petfit.infra.repositories.in_memory.in_memory_recipe_repository import InMemoryRecipeRepository
from petfit.usecases.recipe.create_recipe import CreateRecipeUseCase
from petfit.usecases.recipe.delete_recipe import DeleteRecipeUseCase
from petfit.usecases.recipe.get_all_recipes import GetAllRecipesUseCase
from petfit.usecases.recipe.get_recipe_by_id import GetRecipeByIdUseCase



def create_test_recipe() -> Recipe:
    return Recipe(
        id=str(uuid.uuid4()),
        title="Título de Exemplo",
        ingredients="Conteúdo do r",
        instructions="Descrição de Exemplo",
        img_url="http:/",
        category="gato",
    )


def test_create_post():
    repo = InMemoryRecipeRepository()
    usecase = CreateRecipeUseCase(repo)
    recipe = create_test_recipe()

    result = usecase.execute(recipe)

    assert result == recipe
    assert repo.get_by_id(recipe.id) == recipe


def test_get_all_posts():
    repo = InMemoryRecipeRepository()
    recipe1 = create_test_recipe()
    recipe2 = create_test_recipe()
    repo.create(recipe1)
    repo.create(recipe2)

    usecase = GetAllRecipesUseCase(repo)
    result = usecase.execute()

    assert len(result) == 2
    assert recipe1 in result
    assert recipe2 in result


def test_get_post_by_id():
    repo = InMemoryRecipeRepository()
    recipe = create_test_recipe()
    repo.create(recipe)

    usecase = GetRecipeByIdUseCase(repo)
    result = usecase.execute(recipe.id)

    assert result == recipe


def test_get_post_by_id_not_found():
    repo = InMemoryRecipeRepository()
    usecase = GetRecipeByIdUseCase(repo)
    result = usecase.execute("id-invalido")

    assert result is None




def test_delete_recipe():
    repo = InMemoryRecipeRepository()
    recipe = create_test_recipe()
    repo.create(recipe)

    usecase = DeleteRecipeUseCase(repo)
    usecase.execute(recipe.id)

    assert repo.get_by_id(recipe.id) is None


def test_delete_post_not_found():
    repo = InMemoryRecipeRepository()
    usecase = DeleteRecipeUseCase(repo)

    # Apenas garantir que não levanta exceção
    usecase.execute("id-invalido")