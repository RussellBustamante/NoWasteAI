from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from cameraScript import camera
import subprocess


app = Flask(__name__)
CORS(app)


@app.route('/run-script', methods=['POST'])
@cross_origin()
def run_script():
    data = request.json
    days = data['days']
    ppm = data['ppm']
    prompt1 = data['prompt1']
    print(days, ppm)
    result = subprocess.run(['python', 'python2.py', str(days), str(ppm), str(prompt1)], capture_output=True, text=True)
    output = result.stdout
    return jsonify({"output": output})

# image
@app.route('/run-script1', methods=['POST'])
@cross_origin()
def run_script1():
    result = subprocess.run(['python', 'python.py'], capture_output=True, text=True)
    output = result.stdout
    return jsonify({"output": output})

@app.route('/run-script2', methods=['POST'])
@cross_origin()
def run_script2():
    result = subprocess.run(['python', 'gasScript.py'], capture_output=True, text=True)
    output = result.stdout
    camera()
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(debug=True)
