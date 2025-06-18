from fastapi import APIRouter, HTTPException
from database.models import UserRegister, UserLogin
from configrations import db
from utils.password_handler import hash_password, verify_password
from utils.jwt_handler import create_access_token
from utils.jwt_handler import create_refresh_token
from utils.jwt_handler import decode_token
from utils.email_sender import send_verification_email
from utils.jwt_handler import create_verify_token

auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

user_collection = db["users"]

@auth_router.post("/register")
async def register(user: UserRegister):
    try:
        if user_collection.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pw = hash_password(user.password)
        user_dict = user.dict()
        user_dict["password"] = hashed_pw
        user_dict["is_verified"] = False

        user_collection.insert_one(user_dict)
        verify_token = create_verify_token({"sub": user.email})
        await send_verification_email(user.email, verify_token)

        return {"message": "User registered successfully. Please check your email to verify."}
    except Exception as e:
        print(f"Error in /register: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@auth_router.post("/login")
async def login(user: UserLogin):
    existing_user = user_collection.find_one({"email": user.email})
    if not existing_user or not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.get("/verify-email")
async def verify_email(token: str):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    result = user_collection.update_one({"email": email}, {"$set": {"is_verified": True}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found or already verified")

    return {"message": "Email verified successfully!"}


@auth_router.post("/refresh")
async def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token, is_refresh=True)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    new_access_token = create_access_token({"sub": email})
    return {"access_token": new_access_token, "token_type": "bearer"}

