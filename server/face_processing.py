from fastapi import APIRouter, WebSocket
import numpy as np
import cv2
from fer import FER

router = APIRouter()

detector = FER()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_bytes()
        np_arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        try:
            # Распознавание эмоций
            emotions = detector.detect_emotions(frame)
            if emotions:
                dominant_emotion = max(
                    emotions[0]["emotions"], key=emotions[0]["emotions"].get
                )
                print(
                    f"Эмоция: {dominant_emotion}"
                )  # Можно отправлять клиенту
        except Exception as e:
            print(f"Ошибка: {e}")

        cv2.imshow("Server", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
