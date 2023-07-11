import cv2 as cv
from flask import Flask, Response
from queue import Queue

app = Flask(__name__)

queue = Queue()


def generate():
    while True:
        frame = queue.get()
        if frame is None:
            continue
        (flag, encodedImage) = cv.imencode(".jpg", frame)
        if not flag:
            continue
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + bytearray(encodedImage) + b"\r\n"
        )


@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")
