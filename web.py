import cv2 as cv
from flask import Flask, Response
from queue import Queue
from websockets.server import serve
from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

queue = Queue()
queue.maxsize = 10


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


def send_message(event, data):
    socketio.emit("message", {"event": event, "data": data})


@app.route("/video")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


def run():
    socketio.run(app, debug=True)
