from pydantic import BaseModel, EmailStr


class SignupRequest(BaseModel):
    """
    This is the data the frontend sends when a user signs up.
    
    Example JSON the frontend sends:
    {
        "email": "user@izone.com",
        "password": "mypassword123",
        "full_name": "Kidist Endashaw"
    }
    
    Pydantic automatically validates this — if email is not a valid
    email format, it rejects the request with a clear error message.
    """
    email: EmailStr
    password: str
    full_name: str | None = None


class LoginRequest(BaseModel):
    """
    This is the data the frontend sends when a user logs in.
    
    Example JSON:
    {
        "email": "user@izone.com",
        "password": "mypassword123"
    }
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    This is what the backend sends back after successful login.
    
    Example JSON the backend returns:
    {
        "access_token": "eyJhbGci...",
        "token_type": "bearer"
    }
    
    The frontend stores this token and sends it with every future request.
    """
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """
    This is the user data the backend returns (safe to show — no password).
    
    Example JSON:
    {
        "id": 1,
        "email": "user@izone.com",
        "full_name": "Kidist Endashaw",
        "role": "user"
    }
    """
    id: int
    email: str
    full_name: str | None
    role: str

    class Config:
        from_attributes = True  # allows reading from SQLAlchemy model directly
