from fastapi import APIRouter, Depends, Security, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.token_validator import get_current_user, validate_token
from src.decorators.log_decorator import log_request_response
from src.config.log_config import logger

router = APIRouter(
    prefix="/protected",
    tags=["Protected"],
    responses={404: {"description": "x_user_id field is required in header"}}
)


@router.get("/get_current_user")
@log_request_response(log_route=True)
async def protected_route(request: Request, detail: dict = Depends(get_current_user)):
    """A basic protected route."""
    
    return {"message": "Access granted", "user": detail}

@router.get("/check_admin_role")
@log_request_response(log_route=True)
async def admin_route(request: Request, detail: dict = Depends(get_current_user)):
    """Route accessible only by users with the 'Admin' role."""
    
    # user = detail.get("user", {})
    # roles = user.get("roles", [])
    # logger.info(f"detail : {detail}")
    # logger.info(f"User : {user}")
    # logger.info(f"roles : {roles}")
    roles = detail.get("roles", [])
    logger.info(f"detail : {detail}")
    logger.info(f"roles : {roles}")
    
    if not roles:
        raise HTTPException(status_code=403, detail="Permission denied")
    # Check if the user has the 'Admin' role
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Permission denied")
    return {"message": "Welcome Admin", "user": detail}

#############
@router.get("/check_for_valid_token", dependencies=[Depends(validate_token)])
async def protected_resource():
    '''
    validate_token is still called as a dependency,
      though the validate_token is not used in the function call.
    '''
    return {"message": "This is a protected resource"}