from fastapi import FastAPI
from .routers.categories import router as categories
from .routers.products import router as products


app = FastAPI()



app.include_router(categories)
app.include_router(products)
@app.get("/")
async def root():
    """
    Корневой маршрут, который показывает, что API работает
    """
    return {"message" : "Home"}

