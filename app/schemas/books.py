from pydantic import BaseModel, Field, ConfigDict


class BookBase(BaseModel):
    title: str = Field(...,min_length=1, max_length=200, example="BookA")
    author: str = Field(...,min_length=1, max_length=100, example="VanA")
    price: float = Field(...,gt=0, example=100000)


class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    author: str | None = Field(None, min_length=1, max_length=100)
    price: float |None = Field(None, gt=0)

class BookResponse(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

    