from http.client import HTTPException

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.crud.user import get_user_by_username, create_user, generate_token
from app.schemas.user import UserLoginReq, UserAuthResponse, UserInfoResponse
from app.utils.response import success_response

# 新闻模块路由
router = APIRouter(prefix="/api/user", tags=["用户"])

# 用户注册
@router.post("/register")
async def register(user_data: UserLoginReq, db: AsyncSession = Depends(get_db)):
    # 注册逻辑: 验证用户是否存在 -> 创建用户 -> 生成 Token -> 响应结果
    # 查询用户是否存在
    user = await get_user_by_username(db, user_data.username)
    if user:
        return {
            "code": 400,
            "message": "用户已存在"
        }

    # 新增用户
    user = await create_user(db, user_data)

    # 生成token
    token = await generate_token(db, user.id)

    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userinfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "email": user.email,
    #             "phone": user.phone
    #         }
    #     }
    # }

    return success_response(
        message="注册成功",
        data=UserAuthResponse(
            token=token,
            user_info=UserInfoResponse.model_validate(user)
        )
    )

