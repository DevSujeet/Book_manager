from src.schemas.base import ProjectBaseModel


class SystemMessage(ProjectBaseModel):
    '''
    can be used to return a message to the user
    '''
    code: int
    message: str
    displayMessage: str