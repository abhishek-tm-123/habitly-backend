from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password,verify_password, create_access_token
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# -------------------------
# Signup
# -------------------------

@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    data: SignupRequest,
    db: AsyncSession = Depends(get_db),
):
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Hash password
    hashed_password = hash_password(data.password)

    # Create user
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hashed_password,
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return {
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


# -------------------------
# Login
# -------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    # Find user
    result = await db.execute(
        select(User).where(User.email == data.email)
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    if not verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create JWT
    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

#---------------
#me
#-----------------

@router.get("/me")
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return{
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email
    }