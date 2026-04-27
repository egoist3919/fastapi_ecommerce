from pydantic import BaseModel, Field, ConfigDict, EmailStr
from decimal import Decimal


class CategoryCreate(BaseModel):
    """"
    Модель для создания и обнавления категории
    Используется в POST и PUT запросах
    """
    name: str = Field(..., min_length=3, max_length=50)
    parent_id: int| None = Field(None, description="ID родительской категории, если есть")

class Category(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=50)
    parent_id: int | None = Field(None, description="ID родительской категории, если есть")
    is_active: bool= Field(..., description="Активность категории")
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    """"
        Модель для создания и обнавления категории
        Используется в POST и PUT запросах
    """
    name: str = Field(..., min_length=3, max_length=100, description="Название товара (3-100 символов)")
    price: Decimal = Field(..., description="Цена товара в рублях", gt=0, decimal_places=2)
    description: str|None = Field(None, max_length=500, description="Описание товара")
    image_url: str | None = Field(None, max_length=200, description="URL изображения товара")
    stock:int = Field(..., description="Количество товара на складе")
    category_id: int = Field(..., description="ID категории")



class Product(BaseModel):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """
    id: int = Field(..., description="Уникальный идентификатор товара")
    name: str = Field(..., description="Название товара")
    description: str | None = Field(None, description="Описание товара")
    price: Decimal = Field(..., description="Цена товара в рублях", gt=0, decimal_places=2)
    image_url: str | None = Field(None, description="URL изображения товара")
    stock: int = Field(..., description="Количество товара на складе")
    category_id: int = Field(..., description="ID категории")
    is_active: bool = Field(..., description="Активность товара")

    model_config = ConfigDict(from_attributes=True)



class User(BaseModel):
    id:int
    email:EmailStr
    is_active: bool
    role:str
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr = Field(description='Email пользователя')
    password: str = Field(min_length=8, description="Пароль пользователя(минимум 8 символов)")
    role:str = Field(default='bayer', pattern= "^(buyer|seller)$", description="Роль: buyer или seller")