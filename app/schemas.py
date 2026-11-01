from pydantic import BaseModel

class CreateAdRequest(BaseModel):
    header: str
    description: str
    price: float
    author: str

class CreateAdResponse(BaseModel):
    id: int

class UpdateAdRequest(BaseModel):
    header: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None

class UpdateAdResponse(BaseModel):
    id: int
    header: str
    description: str
    price: float
    author: str
    publication_date: int

class GetAd(BaseModel):
    id: int
    header: str
    description: str
    price: float
    author: str
    publication_date: int

class AdFilter(BaseModel):
    header: str | None = None
    description: str | None = None
    price: float | None = None
    author: str | None = None
    publication_date: int | None = None

class DeleteAd(BaseModel):
    staus: str = 'deleted'