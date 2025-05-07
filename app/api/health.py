
# api/health.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/health", tags=["Health & Debug"])


@router.get("/")
def health_check():
    """基本健康檢查：確認 API 有回應"""
    return {"status": "ok", "message": "API is healthy"}


@router.get("/ping")
def ping():
    """最簡 ping-pong 測試"""
    return {"message": "pong"}


@router.get("/cookie")
def show_cookie(request: Request):
    """顯示目前收到的 cookie"""
    cookies = dict(request.cookies)
    return {"cookies": cookies}


@router.get("/role")
def test_current_role(request: Request):
    """測試 JWT 中的角色資訊"""
    token = request.cookies.get("access_token")
    if not token:
        return JSONResponse(status_code=401, content={"message": "No token found"})

    import jwt  # 確保你已安裝 PyJWT
    from datetime import timezone
    from jwt import ExpiredSignatureError, InvalidTokenError

    try:
        decoded = jwt.decode(
            token,
            "your-secret-key",  # TODO: 改為從 .env 讀取
            algorithms=["HS256"],
        )
        return {
            "username": decoded.get("sub"),
            "role": decoded.get("role"),
            "exp": decoded.get("exp"),
        }
    except ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"message": "Token expired"})
    except InvalidTokenError:
        return JSONResponse(status_code=401, content={"message": "Invalid token"})
