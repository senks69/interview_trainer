import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# from face_processing import router

app = FastAPI(title="Simple FastAPI Server")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(router)


class User(BaseModel):
    login: str
    password: str


@app.post("/login")
async def login(user: User):
    if user.login == "admin" and user.password == "admin":
        return {"status": True}
    return {"status": False}


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Генерируем уникальное имя файла
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            # Читаем файл частями для больших файлов
            while content := await file.read(1024 * 1024):  # 1MB chunks
                buffer.write(content)
                
        return {
            "status": True,
            "message": "File uploaded successfully",
            "filename": filename,
            "path": file_path
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )

@app.get("/api/images")
async def get_images_list():
    images = []
    for filename in os.listdir("uploads"):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            images.append({
                "name": filename,
                "url": f"/uploads/{filename}",
                "size": os.path.getsize(f"uploads/{filename}")
            })
    return JSONResponse(content={"images": images})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
