from flask import Flask, jsonify, request, abort
import os
import random

app = Flask(__name__)

DIRECTORY_NAME = './test_files'
SENSOR_CONFIG_DIR = './sensor_configs'
SENSOR_IDS = ['sensor1', 'sensor2', 'sensor3']

# Create directory if not exists
os.makedirs(DIRECTORY_NAME, exist_ok=True)
os.makedirs(SENSOR_CONFIG_DIR, exist_ok=True)

# Check wheather or not the directory exists
if not os.path.isdir(DIRECTORY_NAME):
    print("Couldn't find directory files")
    exit(1)

if not os.path.isdir(SENSOR_CONFIG_DIR):
    print("Couldn't find sensors directory")
    exit(1)


# Simulated sensor readings
def get_sensor_value(sensor_id):
    if sensor_id not in SENSOR_IDS:
        return None
    # Simulate temperature or pressure
    return round(random.uniform(10.0, 100.0), 2)


# GET: Simulate reading from a sensor
# curl http://127.0.0.1:5000/sensor/sensor1
@app.route('/sensor/<sensor_id>', methods=['GET'])
def read_sensor(sensor_id):
    value = get_sensor_value(sensor_id)
    if value is None:
        return jsonify({'error': f'Sensor {sensor_id} not found'}), 404
    return jsonify({'sensor_id': sensor_id, 'value': value})

# POST: Create sensor config file
# curl -X POST http://127.0.0.1:5000/sensor/sensor1 \
#     -H "Content-Type: application/json" \
#     -d '{"config": "scale: 2.5\nunit: Celsius"}'
@app.route('/sensor/<sensor_id>', methods=['POST'])
def create_sensor_config(sensor_id):
    if sensor_id not in SENSOR_IDS:
        return jsonify({'error': f'Sensor {sensor_id} not recognized'}), 404

    config_filename = f'{SENSOR_CONFIG_DIR}/{sensor_id}_config.txt'

    if os.path.exists(config_filename):
        return jsonify({'error': 'Configuration file already exists'}), 409

    config_data = request.json.get('config', 'scale: 1.0\nunit: C')

    with open(config_filename, 'w') as config_file:
        config_file.write(config_data)

    return jsonify({'message': f'Configuration for {sensor_id} created'})

# PUT: Update existing sensor config file
# curl -X PUT http://127.0.0.1:5000/sensor/sensor1/sensor1_config.txt \
#     -H "Content-Type: application/json" \
#     -d '{"config": "scale: 1.8\nunit: Fahrenheit"}'
@app.route('/sensor/<sensor_id>/<config_name>', methods=['PUT'])
def update_sensor_config(sensor_id, config_name):
    if sensor_id not in SENSOR_IDS:
        return jsonify({'error': f'Sensor {sensor_id} not recognized'}), 404

    config_filename = f'{SENSOR_CONFIG_DIR}/{config_name}'

    if not os.path.exists(config_filename):
        return jsonify({'error': 'Configuration file does not exist'}), 409

    new_content = request.json.get('config')
    if not new_content:
        return jsonify({'error': 'New configuration content required'}), 400

    with open(config_filename, 'w') as config_file:
        config_file.write(new_content)

    return jsonify({'message': f'Configuration {config_name} updated'})



# Get all files in directory
@app.route('/files',methods=['GET'])
def getAllFiles():
    try:
        files = os.listdir(DIRECTORY_NAME)
        return jsonify({'files' : files})
    except Exception as e:
        return jsonify({'error':str(e)}), 500

# Get the content of the specified <filename>
@app.route('/files/<filename>',methods=['GET'])
def getFile(filename):
    file = f'{DIRECTORY_NAME}/{filename}'
    if not os.path.isfile(file):
        abort(404, description="File not found")
    with open(file, 'r') as file_content:
        content = file_content.read()
    return jsonify({'filename': filename, 'content': content})


# Create a file with a specified name and content
@app.route('/files',methods=['POST'])
def createFile():
    data = request.json
    filename = data.get('filename')
    content = data.get('content', '')

    if not filename:
        return jsonify({'error': 'Filename is required'}), 400

    path = os.path.join(DIRECTORY_NAME, filename)
    if os.path.exists(path):
        return jsonify({'error': 'File already exists'}), 400

    with open(path, 'w') as file:
        file.write(content)

    return jsonify({'message': 'File created', 'filename': filename})


# Genereate a file with a specified content only
@app.route('/files/generate', methods=['POST'])
def createFileContent():
    data = request.json
    content = data.get('content', '')
    filename = f'{generated_index}.txt'
    generated_index += 1
    path = os.path.join(DIRECTORY_NAME, filename)

    with open(path, 'w') as file:
        file.write(content)

    return jsonify({'message': 'File created', 'filename': filename})

# Updated an existing file with new content
@app.route('/files/<filename>',methods=['PUT'])
def updateFile(filename):

    path = f'{DIRECTORY_NAME}/{filename}'
    if not os.path.isfile(path):
        abort(404, description="File not found")

    data = request.json
    content = data.get('content')
    if content is None:
        return jsonify({'error': 'Content is required'}), 400

    with open(path, 'w') as file:
        file.write(content)

    return jsonify({'message': 'File updated', 'filename': filename})


# Delete the specified <filename>
@app.route('/files/<filename>',methods=['DELETE'])
def deleteFile(filename):
    path = f'{DIRECTORY_NAME}/{filename}'
    if not os.path.isfile(path):
        abort(404, description="File not found")
    os.remove(path)
    return jsonify({'message': 'File deleted', 'filename': filename})

if __name__ == '__main__':
 app.run()