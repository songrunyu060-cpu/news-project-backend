from typing import Optional
from pydantic import Field
from app.schemas.base import RequestSchema, ResponseSchema


# ==========================================
# 1. 字段定义层 (Pure Field Mixins)
# 只存放字段定义与校验规则，不继承任何 Schema 基类
# ==========================================
class UserBaseFieldsMixin:
  """账号基础身份字段"""

  username: str = Field(..., max_length=50, description="用户名")


class UserProfileFieldsMixin:
  """用户个人资料字段"""

  nickname: Optional[str] = Field(None, max_length=50, description="昵称")
  avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
  gender: Optional[str] = Field(None, max_length=10, description="性别")
  bio: Optional[str] = Field(None, max_length=500, description="个人简介")


# ==========================================
# 2. 接口应用层 (Schemas)
# 组合 Request/Response 行为配置与所需的字段 Mixin
# ==========================================


# --- 请求结构 (Request) ---
class UserLoginReq(RequestSchema, UserBaseFieldsMixin):
  """用户登录/注册请求"""

  password: str = Field(..., description="密码")


class UserProfileUpdateReq(RequestSchema, UserProfileFieldsMixin):
  """修改个人资料请求 (只需传入想修改的资料字段)"""

  pass

class UserUpdatePasswordReq(RequestSchema):
  """修改密码请求"""
  old_password: str = Field(..., description="旧密码")
  new_password: str = Field(..., description="新密码")


# --- 响应结构 (Response) ---
class UserInfoResponse(
    ResponseSchema, UserBaseFieldsMixin, UserProfileFieldsMixin
):
  """完整的用户信息响应"""

  id: int = Field(..., description="用户ID")


class UserAuthResponse(ResponseSchema):
  """登录/认证成功响应"""

  token: str = Field(..., description="JWT Token")
  user_info: UserInfoResponse