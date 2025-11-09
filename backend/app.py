from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import cv2
import os
import zipfile
import shutil
from werkzeug.utils import secure_filename
import tempfile
from pathlib import Path
import uuid

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_frames(video_path, output_dir):
    """Extract all frames from video and save as PNG files"""
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        raise ValueError("Could not open video file")
    
    frame_count = 0
    success = True
    
    while success:
        success, frame = video.read()
        if success:
            frame_filename = os.path.join(output_dir, f'frame_{frame_count:06d}.png')
            cv2.imwrite(frame_filename, frame)
            frame_count += 1
    
    video.release()
    return frame_count


def create_zip(source_dir, zip_path):
    """Create a zip file from a directory"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/extract', methods=['POST'])
def extract():
    """Extract frames from uploaded video"""
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed types: mp4, avi, mov, mkv'}), 400
    
    try:
        # Generate unique ID for this extraction
        extraction_id = str(uuid.uuid4())
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{extraction_id}_{filename}')
        file.save(video_path)
        
        # Create output directory for frames
        frames_dir = os.path.join(app.config['OUTPUT_FOLDER'], extraction_id)
        os.makedirs(frames_dir, exist_ok=True)
        
        # Extract frames
        frame_count = extract_frames(video_path, frames_dir)
        
        # Create zip file
        zip_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{extraction_id}.zip')
        create_zip(frames_dir, zip_path)
        
        # Clean up temporary files
        os.remove(video_path)
        shutil.rmtree(frames_dir)
        
        return jsonify({
            'success': True,
            'frame_count': frame_count,
            'download_id': extraction_id,
            'message': f'Successfully extracted {frame_count} frames'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download/<download_id>', methods=['GET'])
def download(download_id):
    """Download the zip file containing extracted frames"""
    zip_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{download_id}.zip')
    
    if not os.path.exists(zip_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        response = send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name='frames.zip'
        )
        
        # Schedule cleanup after sending
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(zip_path):
                    os.remove(zip_path)
            except Exception as e:
                print(f"Error cleaning up file: {e}")
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
