from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    link: Mapped[str]
    eec_product_id: Mapped[str]
    stock: Mapped[str]
    description: Mapped[str]
    images: Mapped[List["ProductImages"]] = relationship(back_populates="product")
    old_price: Mapped[Optional[int]]
    special_price: Mapped[int]

class ProductImages(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    product: Mapped["Product"] = relationship(back_populates="images")
    image_url: Mapped[str]
