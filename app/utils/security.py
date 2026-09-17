import bcrypt

# 密码加密
def get_hash_password(password: str) -> str:
    safe_password = password.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(safe_password, bcrypt.gensalt())
    return hashed.decode("utf-8")

# 密码验证：返回值是布尔型
def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(safe_password, hashed_password.encode("utf-8"))
