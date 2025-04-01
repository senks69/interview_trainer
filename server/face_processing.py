from fastapi import APIRouter, WebSocket
import numpy as np
import cv2

router = APIRouter()

# Загрузка модели (выполняется один раз при старте)
emotion_labels = [
    "Нейтрально",
    "Счастье",
    "Грусть",
    "Удивление",
    "Страх",
    "Отвращение",
    "Гнев",
    "Презрение",
]
emotion_net = cv2.dnn.readNetFromONNX(
    "emotion-ferplus-8.onnx"
)  # Путь к файлу модели


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Qweqweqweqw")

    while True:
        try:
            # Получаем кадр от клиента
            data = await websocket.receive_bytes()
            frame = cv2.imdecode(
                np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR
            )

            # Подготовка кадра для модели
            blob = cv2.dnn.blobFromImage(
                frame,
                scalefactor=1.0,
                size=(64, 64),  # FER+ ожидает 64x64
                mean=(0.5, 0.5, 0.5),
                swapRB=True,
            )

            # Предсказание эмоции
            emotion_net.setInput(blob)
            outputs = emotion_net.forward()
            emotion_idx = np.argmax(outputs)
            emotion = emotion_labels[emotion_idx]
            print("--->", emotion)
            await websocket.send_text(f"Emotion: {emotion}")

        except Exception as e:
            print(f"Error: {e}")
            break
