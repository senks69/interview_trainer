import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from face_processing import router

app = FastAPI(title="Simple FastAPI Server")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


class User(BaseModel):
    login: str
    password: str


@app.post("/login")
async def login(user: User):
    if user.login == "admin" and user.password == "admin":
        return {"status": True}
    return {"status": False}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
