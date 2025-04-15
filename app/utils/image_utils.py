import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if not file or not file.filename:
        return None
        
    try:
        if not allowed_file(file.filename):
            return None
            
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{uuid.uuid4()}.{ext}"
        
        # Changed path to use static/uploads directly from project root
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, new_filename)
        file.save(file_path)  # Add this line to actually save the file
        return new_filename
        
    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return None

def save_images(files):
    """Save multiple images and return comma-separated filenames"""
    if not files:
        return None
        
    saved_files = []
    for file in files.getlist('images'):
        if file.filename:
            filename = save_image(file)
            if filename:
                saved_files.append(filename)
                
    return ','.join(saved_files) if saved_files else None