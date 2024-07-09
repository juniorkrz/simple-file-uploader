import os
import uuid
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = '/app/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if not request.data:
        return jsonify({"error": "No file part"}), 400

    filename = request.headers.get('Content-Disposition').split('filename=')[1].strip('"')
    if filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file_id = str(uuid.uuid4())
    file_extension = filename.rsplit('.', 1)[1].lower()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id + '.' + file_extension)

    with open(file_path, 'wb') as f:
        f.write(request.data)

    response_data = {
        "file_id": file_id,
        "file_format": file_extension
    }
    return jsonify(response_data), 201

@app.route('/view/<file_id>', methods=['GET'])
def view_file(file_id):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run()
