from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def list():
    pass

@router.post("/")
def create():
    pass

@router.delete("/{review_id}")
def delete(review_id: int):
    pass