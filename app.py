from flask import Flask,render_template,Response,jsonify
import cv2
import ping3
import speedtest


app=Flask(__name__)
camera=cv2.VideoCapture(0)

@app.route('/ping')
def ping():
    host_to_ping = '192.168.1.12'
    latency = ping3.ping(host_to_ping)  
    if latency is not None:
        return jsonify(latency=latency)
    else:
        return jsonify(latency=None, error="Failed to ping the host")

@app.route('/speedtest')
def speedtest_server():
    st = speedtest.Speedtest()
    download_speed = st.download() / 10**6
    return jsonify(speed=download_speed)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)
