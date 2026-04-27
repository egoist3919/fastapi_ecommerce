from app.database import Base
from decimal import Decimal
from sqlalchemy import String, Integer, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    name: Mapped[str]= mapped_column(String(100), nullable=False)
    description: Mapped[str|None]= mapped_column(String(500), nullable=True)
    image_url:Mapped[str|None]= mapped_column(String(100), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)

    category:Mapped["Category"]= relationship("Category", back_populates="products")
    seller_id:Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id:Mapped[int]= mapped_column(ForeignKey("categories.id"), nullable=False)
    seller:Mapped['User'] = relationship("User", back_populates="products")
