from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, asc
from src.models.user import User
from src.schemas.user import UserCreate, UserResponse
from src.crud.base_curd import BaseCRUD
from src.schemas.pagination.pagination import PageParams, paginate

class UserCRUD(BaseCRUD):
    def all_users(self, page_params:PageParams):
        query = self.db_session.query(User).order_by(asc(User.name))
        return paginate(page_params=page_params, query=query, ResponseSchema=UserResponse, model=User)
        

    def get_user_by_id(self, id:str):
        if not id:
            raise HTTPException(status_code=400, detail="User ID must be provided")
    
        filters = [User.id == id]
        query = self.db_session.query(User).filter(and_(*filters)).order_by(asc(User.submitted_date))
        user = query.first()
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    
    def create_user_entry(self, user: UserCreate):
        try:
            user_obj = User(**user.model_dump(exclude={}))
            self.db_session.add(user_obj)
            print(f'create_user in crud post {user_obj}')
            self.db_session.flush()
            self.db_session.commit()
            self.db_session.refresh(user_obj)
            print(f'user is created {user_obj.__dict__}')
            user_dict = user_obj.__dict__.copy()
            user_dict.pop("_sa_instance_state", None)  # Remove SQLAlchemy internal state
            return user_dict
        except IntegrityError as e:
            print(f"IntegrityError: {e}")  # Log the full exception
            print(f"Exception details: {e.orig}")  # Print out the underlying database exception details

            # Handle SQLite unique constraint violation
            if "UNIQUE constraint failed" in str(e.orig):
                print("Unique constraint failed: user already exists.")
                raise HTTPException(status_code=400, detail="user email already exists")
            
            # Catch other IntegrityErrors and re-raise with a generic error
            raise HTTPException(status_code=500, detail="Internal Server Error")
        except Exception as e:
            # This will catch any unexpected exceptions that are not specifically caught by the above blocks
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def delete_user_by_id(self, id:str):
        user = self.get_user_by_id(id=id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return user
        else:
            raise HTTPException(status_code=404, detail="user not found")