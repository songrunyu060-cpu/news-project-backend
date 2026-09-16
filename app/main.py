from fastapi import FastAPI
from app.routers import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许所有来源
    allow_credentials=True, # 允许携带Cookie
    allow_methods=["*"], # 允许所有方法
    allow_headers=["*"], # 允许所有头
)

# 注册路由
app.include_router(news.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
