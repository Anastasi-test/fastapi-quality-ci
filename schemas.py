from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    """
    Базовая схема рецепта.
    """
    name: str = Field(..., description="Название блюда", min_length=1, max_length=200)
    cooking_time: int = Field(..., description="Время приготовления в минутах", gt=0)
    ingredients: str = Field(..., description="Список ингредиентов")
    description: str = Field(..., description="Описание процесса приготовления")


class RecipeIn(RecipeBase):
    """
    Схема для создания нового рецепта.
    """
    pass


class RecipeOut(BaseModel):
    """
    Схема краткой информации о рецепте (первый экран).
    """
    id: int = Field(..., description="ID рецепта")
    name: str = Field(..., description="Название блюда")
    views_count: int = Field(..., description="Количество просмотров")
    cooking_time: int = Field(..., description="Время приготовления")

    class Config:
        orm_mode = True


class RecipeDetail(RecipeBase):
    """
    Схема детальной информации о рецепте (второй экран).
    """
    id: int = Field(..., description="ID рецепта")
    views_count: int = Field(..., description="Количество просмотров")

    class Config:
        orm_mode = True
