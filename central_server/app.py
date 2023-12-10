from flask import Flask, request, jsonify, send_file
from content_manager import ContentManager

app = Flask(__name__)
content_manager = ContentManager()

@app.route('/content/<filename>', methods=['GET'])
def content(filename):
    content = content_manager.retrieve_content(filename)
    if content is not None:
        content_manager.increment_download(filename) 
        return send_file(f"static/{filename}", as_attachment=True, download_name=filename), 200
    else:
        jsonify({"message": "Content not found."}), 404
        
@app.route('/fetch/<filename>', methods=['GET'])
def fetch(filename):
    content = content_manager.retrieve_content(filename)
    if content is not None:
        return send_file(f"static/{filename}", as_attachment=True, download_name=filename), 200
    else:
        jsonify({"message": "Content not found."}), 404
        
@app.route('/download_increment/<filename>', methods=['POST'])
def increment_download(filename):
    content_manager.increment_download(filename)
    return jsonify({"message:" f"Incremented download for file: {filename}"}), 200

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file uploads.
    Receives a file from the request and passes it to the content manager.
    Returns a JSON response indicating success or failure.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    content_manager.upload_content(file)
    return jsonify({"message": "Content uploaded successfully"}), 201

@app.route('/delete/<filename>', methods=['DELETE'])
def delete(filename):
    """
    Handle file deletions.
    Deletes a file specified by 'filename' from the server.
    Returns a JSON response indicating success or failure.
    """
    try:
        content_manager.delete_content(filename)
        return jsonify({"message": "Content deleted successfully"}), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/list', methods=['GET'])
def list_content():
    """
    List all files in the content directory.
    Retrieves the list of files from the content manager and returns it in a JSON response.
    """
    content = content_manager.list_content()
    return jsonify({"content": content}), 200

@app.route('/popular/<int:limit>', methods=['GET'])
def popular_content(limit):
    popular_files = content_manager.get_popular_content(limit)
    return jsonify({"content":popular_files}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
