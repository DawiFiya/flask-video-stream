from flask import Flask, Response
import cv2

app = Flask(__name__)

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

# 🔹 Route to access the video stream
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run Flask app on port 5000
