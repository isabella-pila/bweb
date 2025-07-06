from fastapi import APIRouter, HTTPException, Depends
from petfit.usecases.recipe.create_recipe import CreaterecipeUseCase
from petfit.usecases.recipe.delete_recipe import DeleteRecipeUseCase
from petfit.usecases.recipe.get_all_recipes import GetAllrecipesUseCase
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
from petfit.infra.repositories.sqlalchemy.sqlachemy_user_repository import (
    SQLAlchemyRecipeRepository,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
router = APIRouter()


@router.get("/", response_model=List[RecipeOutput])
async def get_all_recipes(
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
):
    usecase = GetAllrecipesUseCase(recipe_repo)
    recipes = await usecase.execute()
    return recipes


@router.get("/{recipe_id}", response_model=RecipeOutput)
async def get_recipe_by_id(
    recipe_id: str,
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase = GetRecipeByIdUseCase(recipe_repo)
    recipe = await usecase.execute(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="recipe not found")
    return recipe


@router.recipe("/", response_model=RecipeOutput)
async def create_recipe(
    data: RecipeCreateInput,
    db: AsyncSession = Depends(get_db_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user: str = Depends(get_current_user),
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
):
    usecase = CreaterecipeUseCase(recipe_repo)
    if data.date.tzinfo is not None:
        data.date = data.date.replace(tzinfo=None)
    recipe = Recipe(
        id=str(uuid.uuid4()),
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=user.id,
        date=data.date,
    )
    created_recipe = await usecase.execute(recipe)
    return created_recipe


@router.put("/{recipe_id}", response_model=RecipeOutput)
async def update_recipe(
    recipe_id: str,
    data: RecipeUpdateInput,
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase_get = GetRecipeByIdUseCase(recipe_repo)
    existing_recipe = await usecase_get.execute(recipe_id)
    if not existing_recipe:
        raise HTTPException(status_code=404, detail="recipe not found")

    updated_recipe = Recipe(
        id=recipe_id,
        title=data.title,
        description=data.description,
        content=data.content,
        user_id=existing_recipe.user_id,
        date=existing_recipe.date,
    )
    usecase_update = update_recipe(recipe_repo)
    result = await usecase_update.execute(updated_recipe)
    return result


@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: str,
    recipe_repo: RecipeRepository = Depends(get_recipe_repository),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    usecase = DeleteRecipeUseCase(recipe_repo)
    success = await usecase.execute(recipe_id)
    if not success:
        raise HTTPException(status_code=404, detail="recipe not found")
    return {"message": "recipe deleted successfully"}