from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, asc
from src.models.user_book_review import UserBookReview
from src.schemas.user_book_review import UserBookReviewCreate, UserBookReviewResponse, UserBookReviewUpdate
from src.crud.base_curd import BaseCRUD
from src.schemas.pagination.pagination import PageParams, paginate

class UserBookReviewCRUD(BaseCRUD):
    # def all_users(self, page_params:PageParams):
    #     query = self.db_session.query(User).order_by(asc(User.name))
    #     return paginate(page_params=page_params, query=query, ResponseSchema=UserResponse, model=User)
        

    def get_user_review_by_id(self, id:str):
        if not id:
            raise HTTPException(status_code=400, detail="User ID must be provided")
    
        filters = [UserBookReview.id == id]
        query = self.db_session.query(UserBookReview).filter(and_(*filters)).order_by(asc(UserBookReview.submitted_date))
        user = query.first()
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    
    def create_user_book_reivew_entry(self, review: UserBookReviewCreate):
        try:
            user_review_obj = UserBookReview(**review.model_dump(exclude={}))
            self.db_session.add(user_review_obj)
            print(f'create_user in crud post {user_review_obj}')
            self.db_session.flush()
            self.db_session.commit()
            self.db_session.refresh(user_review_obj)
            print(f'user is created {user_review_obj.__dict__}')
            user_review_dict = user_review_obj.__dict__.copy()
            user_review_dict.pop("_sa_instance_state", None)  # Remove SQLAlchemy internal state
            return user_review_dict
        except IntegrityError as e:
            print(f"IntegrityError: {e}")  # Log the full exception
            print(f"Exception details: {e.orig}")  # Print out the underlying database exception details

            # Handle sql unique constraint violation
            if "UNIQUE constraint failed" in str(e.orig):
                print("Unique constraint failed: user already exists.")
                raise HTTPException(status_code=400, detail="review already exists")
            
            # Catch other IntegrityErrors and re-raise with a generic error
            raise HTTPException(status_code=500, detail="Internal Server Error")
        except Exception as e:
            # This will catch any unexpected exceptions that are not specifically caught by the above blocks
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def delete_user_review_by_id(self, id:str):
        review = self.get_user_review_by_id(id=id)
        if review:
            self.db_session.delete(review)
            self.db_session.commit()
            return review
        else:
            raise HTTPException(status_code=404, detail="review not found")
        
    def update_user_book_review(self, id:str, review:UserBookReviewUpdate):
        # Get the existing review
        existing_review = self.get_user_review_by_id(id=id)
        if not existing_review:
            raise HTTPException(status_code=404, detail="review not found")
        
        # Update the review with new data
        for key, value in review.model_dump(exclude={}).items():
            setattr(existing_review, key, value)
        
        # Commit the changes to the database
        self.db_session.commit()
        self.db_session.refresh(existing_review)
        
        return existing_review