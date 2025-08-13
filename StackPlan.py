from flask import Flask, request, jsonify, send_from_directory
import os
import time

app = Flask(__name__)
port = 3000

UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload-svg', methods=['POST'])
def upload_svg():
    svg_data = request.data.decode('utf-8')

    if not svg_data or not svg_data.startswith('<svg'):
        return jsonify({'error': 'Invalid SVG data.'}), 400

    filename = f"svg-{int(time.time() * 1000)}.svg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_data)
    except Exception as e:
        return jsonify({'error': f'Could not save SVG file: {str(e)}'}), 500

    file_url = f"https://localhost:{port}/upload/{filename}"
    return jsonify({'message': 'SVG uploaded', 'url': file_url})

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(port=port)
