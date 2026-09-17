from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response[T](code: int = 200, message: str = "success", data: T = None):
    # 把任何的fastapi对象 pydantic, ORM对象 转换为 JSON 响应对象
    return JSONResponse(
        status_code=code,
        content=jsonable_encoder(
            {
                "code": code,
                "message": message,
                "data": data
            }
        )
    )