from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import User
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserResponse


def signup_user(request: SignupRequest, db: Session) -> UserResponse:
    """
    Creates a new user account.
    
    Steps:
    1. Check if email already exists → if yes, reject with error
    2. Hash the password → never store plain text
    3. Create the user in the database
    4. Return the user data (without password)
    """

    # Step 1 — Check if email already taken
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Step 2 — Hash the password
    hashed = hash_password(request.password)

    # Step 3 — Create user in database
    new_user = User(
        email=request.email,
        hashed_password=hashed,
        full_name=request.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Step 4 — Return user (Pydantic converts it automatically)
    return UserResponse.model_validate(new_user)


def login_user(request: LoginRequest, db: Session) -> TokenResponse:
    """
    Logs in a user and returns a JWT token.
    
    Steps:
    1. Find user by email → if not found, reject
    2. Verify password → if wrong, reject
    3. Create JWT token with user's email
    4. Return the token
    """

    # Step 1 — Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Step 2 — Check password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Step 3 — Create token (sub = subject = who this token belongs to)
    token = create_access_token(data={"sub": user.email})

    # Step 4 — Return token
    return TokenResponse(access_token=token)
