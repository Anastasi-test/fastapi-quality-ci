from sqlalchemy import Column, Integer, String, Text

from database import Base


class Recipe(Base):
    """
    Модель рецепта в базе данных.
    """
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True, comment="Название блюда")
    views_count = Column(Integer, default=0, nullable=False, comment="Количество просмотров")
    cooking_time = Column(Integer, nullable=False, comment="Время приготовления в минутах")
    ingredients = Column(Text, nullable=False, comment="Список ингредиентов")
    description = Column(Text, nullable=False, comment="Описание процесса приготовления")
