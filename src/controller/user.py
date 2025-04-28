
from fastapi import HTTPException
from src.db import get_session
from src.schemas.user import UserCreate
from src.crud.user import UserCRUD
from src.schemas.pagination.pagination import PageParams

def all_users(user_id:str, page_params:PageParams):
    with get_session() as session:
        book = UserCRUD(db_session=session).all_users(page_params=page_params)
        return book

def get_user_by_id(user_id:str, id:str):
     with get_session() as session:
        book = UserCRUD(db_session=session).get_user_by_id(id=id)
        if not book:
            raise HTTPException(status_code=404, detail="User not found")
        return book

def create_user_entry(user_id: str, user:UserCreate):
    with get_session() as session:
        user_obj = UserCRUD(db_session=session).create_user_entry(user=user)
        if not user_obj:
            raise HTTPException(status_code=400, detail="user creation failed")
        return user_obj
    

def delete_user_by_id(user_id:str, id:str):
    with get_session() as session:
        book = UserCRUD(db_session=session).get_user_by_id(id=id)
        if not book:
            raise HTTPException(status_code=404, detail="user not found")
        return book