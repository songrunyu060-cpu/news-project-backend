import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserToken
from app.schemas.user import UserLoginReq
from app.utils.security import get_hash_password


# 根据用户名获取用户
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(User)
            .where(User.username == username)
    )
    return result.scalar_one_or_none()

# 创建用户
async def create_user(db: AsyncSession, user_data: UserLoginReq):
    # 生成加密密码
    hash_password = get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hash_password)
    db.add(user)
    await db.commit()
    # refresh 刷新用户数据，确保用户数据最新
    await db.refresh(user)
    return user

# 生成token
async def generate_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())
    expires = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expires
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires)
    db.add(user_token)
    await db.commit()
    await db.refresh(user_token)
    return user_token.token
