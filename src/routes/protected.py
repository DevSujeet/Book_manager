from fastapi import APIRouter, Depends, Security, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.token_validator import get_current_user, validate_token
from src.decorators.log_decorator import log_request_response


router = APIRouter(
    prefix="/protected",
    tags=["Protected"],
    responses={404: {"description": "x_user_id field is required in header"}}
)


@router.get("/get_current_user")
@log_request_response(log_route=True)
async def protected_route(request: Request, user: dict = Depends(get_current_user)):
    """A basic protected route."""
    
    return {"message": "Access granted", "user": user}

@router.get("/check_admin_role")
@log_request_response(log_route=True)
async def admin_route(user: dict = Depends(get_current_user)):
    """Route accessible only by users with the 'Admin' role."""
    roles = user.get("roles", [])
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Welcome Admin", "user": user}

#############
@router.get("/check_for_valid_token", dependencies=[Depends(validate_token)])
async def protected_resource():
    '''
    validate_token is still called as a dependency,
      though the validate_token is not used in the function call.
    '''
    return {"message": "This is a protected resource"}