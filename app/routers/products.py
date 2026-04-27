from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update

from app.models.products import Product as ProductModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.models.categories import Category as CategoryModel

from app.db_depends import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductSchema], status_code=status.HTTP_200_OK)
async def get_all_products(db:AsyncSession= Depends(get_async_db)):
    """
    Возвращает список всех товаров.(уже асинхронно)
    """
    stmt= select(ProductModel).where(ProductModel.is_active==True)
    res = await db.scalars(stmt)

    return res.all()


@router.post("/", response_model=ProductSchema)
async def create_product(product:ProductCreate, db:AsyncSession= Depends(get_async_db)):
    """
    Создаёт новый товар.(уже асинхронно)
    """

    category = await db.scalars(select(CategoryModel).where(CategoryModel.id == product.category_id).where(CategoryModel.is_active==True))
    if category.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail= "Category not found or inactive")

    db_product= ProductModel(**product.model_dump())
    db.add(db_product)
    await db.commit()
    return db_product


@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(category_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список активных товаров в указанной категории по её ID.
    """
    # Проверяем, существует ли активная категория
    result = await db.scalars(
        select(CategoryModel).where(CategoryModel.id == category_id,
                                    CategoryModel.is_active == True)
    )
    category = result.first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Category not found or inactive")

    # Получаем активные товары в категории
    product_result = await db.scalars(
        select(ProductModel).where(ProductModel.category_id == category_id, ProductModel.is_active == True)
    )
    return product_result.all()



@router.get("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db:AsyncSession=Depends(get_async_db)):
    """
    Возвращает детальную информацию о товаре по его ID.(уже асинхроно)
    """
    product_stmt= select(ProductModel).where(ProductModel.id==product_id).where(ProductModel.is_active==True)
    res = await db.scalars(product_stmt)
    product = res.first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found or inactive")


    category_stmt= select(CategoryModel).where(CategoryModel.id == product.category_id).where(CategoryModel.is_active==True)
    res = await db.scalars(category_stmt)
    category = res.first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found or inactive")
    return product


@router.put("/{product_id}")
async def update_product(product_id: int, product:ProductCreate, db:AsyncSession= Depends(get_async_db)):
    """
    Обновляет товар по его ID.(уже асинхронно)
    """
    product_stmt= select(ProductModel).where(ProductModel.id == product_id).where(ProductModel.is_active == True)
    res = await db.scalars(product_stmt)
    db_product = res.first()
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found or inactive")

    category_stmt = select(CategoryModel).where(CategoryModel.id == product.category_id).where(CategoryModel.is_active == True)
    res = await db.scalars(category_stmt)
    db_category = res.first()
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found or inactive")

    await db.execute(update(ProductModel).where(ProductModel.id == product_id).values(**product.model_dump()))
    await db.commit()
    return db_product



@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db:AsyncSession= Depends(get_async_db)):
    """
    Удаляет товар по его ID.
    """
    stmt= select(ProductModel).where(ProductModel.id==product_id).where(ProductModel.is_active==True)
    res = await db.scalars(stmt)
    product = res.first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found or inactive")

    await db.execute(update(ProductModel).where(ProductModel.id == product_id).values(is_active=False))
    await db.commit()
    return product


