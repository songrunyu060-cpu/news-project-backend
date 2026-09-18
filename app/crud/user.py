import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserToken
from app.schemas.user import UserLoginReq, UserProfileUpdateReq
from app.utils.security import get_hash_password, verify_password


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

# 验证用户
async def verify_user(db: AsyncSession, user: UserLoginReq):
    db_user = await get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        return None
    return db_user

# 根据token查询用户 返回用户信息
async def get_user_by_token(db: AsyncSession, token: str):
    query = (
        select(User)
        .join(UserToken, User.id == UserToken.user_id)
        .where(UserToken.token == token, UserToken.expires_at > datetime.now())
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 修改用户信息
async def update_user_profile(db: AsyncSession, username: str, user_data: UserProfileUpdateReq):
    query = (
        update(User)
             .where(User.username == username)
             .values(user_data.model_dump(
                 exclude_unset=True,
                 exclude_none=True
            )
        )
    )
    result = await db.execute(query)
    await db.commit()
    # 检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取一下更新后的用户
    updated_user = await get_user_by_username(db, username)
    return updated_user
