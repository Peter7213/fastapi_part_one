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
    publication_date: str

class GetAd(BaseModel):
    id: int
    header: str
    description: str
    price: float
    author: str
    publication_date: str

class DeleteAd(BaseModel):
    staus: str = 'deleted'