from fastapi import FastAPI, Response, Request
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2 as cv
import uvicorn
import asyncio
import time

app = FastAPI(debug=True)

cap = cv.VideoCapture(0)

async def generate():
    global cap  # Use the global video capture instance

    while True:
        print("start", time.time())
        start_time = time.time() 
        ret, frame = cap.read()
        if not ret:
            break
        elapsed_time = time.time() - start_time
        encoded_frame = cv.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n')
        remaining_time = max(0, 1 / 30 - elapsed_time) 
        print("end",time.time())
        print(elapsed_time)
        await asyncio.sleep(remaining_time)

@app.get("/test1")
async def root():
    return "Hello World!"

@app.get('/')
async def video_feed():
    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
