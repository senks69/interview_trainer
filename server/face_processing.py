from fastapi import APIRouter, WebSocket
import numpy as np
import cv2
import asyncio

router = APIRouter()

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
emotion_net = cv2.dnn.readNetFromONNX("emotion-ferplus-8.onnx")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket подключен")

    while True:
        try:
            data = await websocket.receive_bytes()
            frame = cv2.imdecode(
                np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR
            )

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (64, 64))
            frame = frame[np.newaxis, np.newaxis, :, :]

            blob = (frame.astype(np.float32) - 128) / 128

            emotion_net.setInput(blob)
            outputs = emotion_net.forward()
            emotion_idx = np.argmax(outputs)
            emotion = emotion_labels[emotion_idx]
            await websocket.send_text(f"Emotion: {emotion}")

            await asyncio.sleep(1)

        except Exception as e:
            print(f"Error: {e}")
            break
