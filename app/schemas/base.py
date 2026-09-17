from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


# ==========================================
# 1. 通用根基类 (基础数据清洗与类型兼容)
# ==========================================
class BaseSchema(BaseModel):
  """所有 Schema 的最底层基类

  解决通用数据清洗和类型问题
  """

  model_config = ConfigDict(
      # 自动过滤字符串首尾多余的空格（如输入 " admin " 自动清洗为 "admin"）
      str_strip_whitespace=True,
      # 提取枚举字段时直接拿到 raw value (如 'admin' 而不是 <Role.ADMIN: 'admin'>)
      use_enum_values=True,
      # 允许赋值未定义的自定义类型对象
      arbitrary_types_allowed=True,
  )


# ==========================================
# 2. API 请求基类 (入参校验与安全性控制)
# ==========================================
class RequestSchema(BaseSchema):
  """专门用于接收前端参数的 Schema (POST/PUT/PATCH 请求)"""

  model_config = ConfigDict(
      # 禁止传入未在模型中定义的额外参数（防止脏数据注入）
      extra='forbid',
      # 允许使用属性名赋值，同时也兼容前端传入的 alias
      populate_by_name=True,
  )


# ==========================================
# 3. API 响应基类 (自动转换与 ORM 兼容)
# ==========================================
class ResponseSchema(BaseSchema):
  """专门用于给前端返回数据的 Schema (API Response)"""

  model_config = ConfigDict(
      # 1. 自动支持将 SQLAlchemy / SQLModel 等 ORM 对象转为 Pydantic 实例
      from_attributes=True,
      # 2. 自动将 Python 蛇形命名 (user_name) 转换为前端驼峰命名 (userName)
      alias_generator=to_camel,
      # 3. 允许在 Python 端直接使用字段属性名 (user_name) 实例化对象
      populate_by_name=True,
  )