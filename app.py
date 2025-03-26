from flask import Flask, Response
from flask_cors import CORS  # Import CORS to enable cross-origin access
import cv2

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# 🔹 Replace with your ESP32-CAM Stream URL (Find the IP from Serial Monitor)
ESP32_STREAM_URL = "http://172.20.10.2:81/stream"

def generate_frames():
    cap = cv2.VideoCapture(ESP32_STREAM_URL)  # Open video stream
    while True:
        success, frame = cap.read()  # Read frame from ESP32-CAM
        if not success:
            break
        else:
            _, buffer = cv2.imencode('.jpg', frame)  # Convert frame to JPEG
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Send frame

# 🔹 Basic route to check if the server is running
@app.route('/')
def home():
    return "Flask Server is Running! Go to /video_feed to see the stream."

# 🔹 Route to access the video stream
@app.route('/video_feed')
def video_feed():
    response = Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run Flask app on port 5000
