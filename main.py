import models

from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from database import Base, engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events приложения.
    Создание таблиц при старте и освобождение ресурсов при завершении.
    """
    async with engine.begin() as conn:
        def create_tables(sync_conn):
            Base.metadata.create_all(bind=sync_conn)
        await conn.run_sync(create_tables)
    yield
    await engine.dispose()


app = FastAPI(
    title="Кулинарная книга API",
    description="""
    API сервиса кулинарной книги.

    Возможности:
    - Получение списка рецептов, отсортированных по популярности
    - Получение детальной информации о рецепте
    - Создание новых рецептов

    При каждом просмотре детального рецепта увеличивается счётчик просмотров.
    """,
    version="1.0.0",
    lifespan=lifespan,
)


@app.post(
    "/recipes",
    response_model=schemas.RecipeDetail,
    status_code=201,
    summary="Создать новый рецепт",
)
async def create_recipe(
    recipe: schemas.RecipeIn,
    session: AsyncSession = Depends(get_session),
):
    """
    Создаёт новый рецепт в базе данных.
    """
    new_recipe = models.Recipe(**recipe.dict())
    session.add(new_recipe)
    await session.commit()
    await session.refresh(new_recipe)
    return new_recipe


@app.get(
    "/recipes",
    response_model=List[schemas.RecipeOut],
    summary="Получить список всех рецептов",
)
async def get_recipes(
    session: AsyncSession = Depends(get_session),
):
    """
    Возвращает список всех рецептов, отсортированных по:
    1. количеству просмотров (по убыванию)
    2. времени приготовления (по возрастанию)
    """
    query = select(models.Recipe).order_by(
        desc(models.Recipe.views_count),
        models.Recipe.cooking_time,
    )
    result = await session.execute(query)
    return result.scalars().all()


@app.get(
    "/recipes/{recipe_id}",
    response_model=schemas.RecipeDetail,
    summary="Получить детальную информацию о рецепте",
)
async def get_recipe(
    recipe_id: int = Path(..., ge=1, description="ID рецепта"),
    session: AsyncSession = Depends(get_session),
):
    """
    Возвращает детальную информацию о рецепте.
    При каждом запросе увеличивает счётчик просмотров.
    """
    result = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = result.scalar_one_or_none()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    recipe.views_count += 1
    await session.commit()
    await session.refresh(recipe)

    return recipe
