from fastapi import APIRouter, HTTPException, Depends
from petfit.usecases.recipe.create_recipe import CreateRecipeUseCase
from petfit.usecases.recipe.delete_recipe import DeleteRecipeUseCase
from petfit.usecases.recipe.get_all_recipes import GetAllRecipesUseCase
from petfit.usecases.recipe.get_recipe_by_id import GetRecipeByIdUseCase

from petfit.domain.entities.recipe import Recipe
from petfit.domain.entities.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from petfit.api.deps import (
    get_user_repository,
    get_current_user,
    get_db_session,
    get_recipe_repository,
)
from typing import List
from petfit.domain.repositories.recipe_repository import RecipeRepository

from petfit.api.schemas.recipe_schema import RecipeCreateInput

import uuid
from petfit.api.schemas.recipe_schema import RecipeOutput, RecipeCreateInput, RecipeUpdateInput
from petfit.infra.repositories.sqlalchemy.sqlalchemy_recipe_repository import (
    SQLAlchemyRecipeRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from petfit.api.schemas.recipe_schema import recipe_to_output, recipes_to_output

security = HTTPBearer()
router = APIRouter()


@router.get("/", response_model=List[RecipeOutput])
async def get_all_recipes(
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
):
    usecase = GetAllRecipesUseCase(recipe_repo)
    recipes = await usecase.execute()
    return recipes_to_output(recipes)


@router.get("/{recipe_id}", response_model=RecipeOutput)
async def get_recipe_by_id(
    recipe_id: str,
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
):
    usecase = GetRecipeByIdUseCase(recipe_repo)
    recipe = await usecase.execute(recipe_id)
    print(f"Retrieved recipe: {recipe}")
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_to_output(recipe)

@router.post("/", response_model=RecipeOutput)
async def create_recipe(
    data: RecipeCreateInput,
    db: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: User = Depends(get_current_user),
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
):
    usecase = CreateRecipeUseCase(recipe_repo)
    if data.date.tzinfo is not None:
        data.date = data.date.replace(tzinfo=None)
    recipe = Recipe(
        id=str(uuid.uuid4()),
        title=data.title,
        ingredients=data.ingredients,
        instructions=data.instructions,
        category=data.category,
        img_url=data.img_url,
    )
    created_recipe = await usecase.execute(recipe)
    if not created_recipe:
        raise HTTPException(status_code=404, detail="Recipe not created")
    return recipe_to_output(created_recipe)


@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: str,
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase = DeleteRecipeUseCase(recipe_repo)
    success = await usecase.execute(recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {"message": "Recipe deleted successfully"}