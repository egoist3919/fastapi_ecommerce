from fastapi import FastAPI
from .routers.categories import router as categories
from .routers.products import router as products
from .routers.users import router as users

app = FastAPI()



app.include_router(categories)
app.include_router(products)
app.include_router(users)
@app.get("/")
async def root():
    """
    Корневой маршрут, который показывает, что API работает
    """
    return {"message" : "Home"}

