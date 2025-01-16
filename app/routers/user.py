from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete
from app.backend.db_depends import get_db
from app.models import User
from app.schemas import CreateUser, UpdateUser
from slugify import slugify

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/user_id")
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        return user
    raise HTTPException(status_code=404, detail="User was not found")

@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(user.username)
    new_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slug
    )
    db.add(new_user)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update")
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalar(select(User).where(User.id == user_id))
    if existing_user:
        db.execute(
            update(User).where(User.id == user_id).values(
                firstname=user.firstname,
                lastname=user.lastname,
                age=user.age
            )
        )
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    raise HTTPException(status_code=404, detail="User was not found")

@router.delete("/delete")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.scalar(select(User).where(User.id == user_id))
    if existing_user:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}
    raise HTTPException(status_code=404, detail="User was not found")

