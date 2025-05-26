from flask import Flask, jsonify, request, abort
import os

app = Flask(__name__)

DIRECTORY_NAME = './test_files'
generated_index = 0
# Check wheather or not the directory exists
if not os.path.isdir(DIRECTORY_NAME):
    print("Couldn't find directory")
    exit(1)


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