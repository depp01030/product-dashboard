from fastapi import APIRouter, HTTPException, status, Form, Header, Depends
from datetime import timedelta, datetime, timezone
from typing import Optional
import jwt

router = APIRouter(prefix="/auth", tags=["Auth"])

MOCK_USERS = {
    "admin": {"password": "amy88954", "role": "admin"},
    "viewer": {"password": "123456", "role": "viewer"},
}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token_from_header(authorization: Optional[str]) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供有效的 Authorization header")

    token = authorization[len("Bearer "):]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": payload.get("sub"),
            "role": payload.get("role"),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已過期")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="無效的 token")


@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
):
    user = MOCK_USERS.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="帳號或密碼錯誤")

    access_token = create_access_token(
        data={"sub": username, "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": access_token,
        "role": user["role"]
    }


@router.get("/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    user_info = verify_token_from_header(authorization)
    return {"role": user_info["role"]}
