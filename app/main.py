from fastapi import FastAPI
from app.routers import news, user
from fastapi.middleware.cors import CORSMiddleware
from app.utils.exception_handlers import register_exception_handlers

app = FastAPI()

# 注册异常处理
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许所有来源
    allow_credentials=True, # 允许携带Cookie
    allow_methods=["*"], # 允许所有方法
    allow_headers=["*"], # 允许所有头
)

# 注册路由
app.include_router(news.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

