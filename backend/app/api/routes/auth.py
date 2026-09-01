from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth import signup_user, login_user
from app.api.deps import get_current_user
from app.db.models import User

# APIRouter groups related endpoints together.
# All routes here will be prefixed with /api/auth
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    CREATE A NEW USER ACCOUNT
    
    Frontend sends:
        POST /api/auth/signup
        {
            "email": "user@izone.com",
            "password": "mypassword123",
            "full_name": "Kidist"
        }
    
    Backend returns:
        {
            "id": 1,
            "email": "user@izone.com",
            "full_name": "Kidist",
            "role": "user"
        }
    """
    return signup_user(request, db)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    LOGIN AND GET A TOKEN
    
    Frontend sends:
        POST /api/auth/login
        {
            "email": "user@izone.com",
            "password": "mypassword123"
        }
    
    Backend returns:
        {
            "access_token": "eyJhbGci...",
            "token_type": "bearer"
        }
    
    The frontend stores this token and sends it with every future request
    in the header: Authorization: Bearer eyJhbGci...
    """
    return login_user(request, db)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    GET CURRENT LOGGED-IN USER INFO
    
    Frontend sends:
        GET /api/auth/me
        Header: Authorization: Bearer eyJhbGci...
    
    Backend returns:
        {
            "id": 1,
            "email": "user@izone.com",
            "full_name": "Kidist",
            "role": "user"
        }
    
    This endpoint is protected — requires a valid token.
    """
    return current_user
