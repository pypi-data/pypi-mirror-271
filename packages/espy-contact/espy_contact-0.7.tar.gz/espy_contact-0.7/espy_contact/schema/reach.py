from typing import List,Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel,Field, EmailStr
from espy_contact.schema.schema import AppuserDto,AddressDto
class ProductBase(BaseModel):
    logo: str
    website: str
    ga_property_id: str
    socials: str
    cost: Decimal = Field(max_digits=10, decimal_places=2)
    expiry_date: Optional[datetime] = None
    note: str

class ProductCreate(ProductBase):
    pass
class Product(ProductBase):
    id: int
    customer_id: int

    class Config:
        orm_mode = True
class CustomerBase(BaseModel):
    pass

class CustomerCreate(CustomerBase):
    business_name: str
    business_email: EmailStr
    contact_name: str
    contact_phone: str
    contact_email: EmailStr
    address: AddressDto
    class Config:
        orm_mode = True

class Customer(CustomerBase):
    id: int
    staff: List[AppuserDto] = []
    products: List[Product] = []

    class Config:
        orm_mode = True