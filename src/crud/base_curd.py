from sqlalchemy.orm import Session
# from sqlmodel import  Session

class BaseCRUD:
    def __init__(self, db_session: Session): 
        self.db_session = db_session

   