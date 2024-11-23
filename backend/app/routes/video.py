# app/routes/video.py
from flask import Blueprint, request, jsonify
from ..services.video_processing import VideoProcessingService
from app import db
from ..models.video import Video

video_bp = Blueprint('video', __name__)

@video_bp.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'status': 'Video routes working!'}), 200

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        if not video_file.filename:
            return jsonify({'error': 'No selected file'}), 400
            
        # Create video processing service
        video_processing = VideoProcessingService()
        
        # Process upload
        video_metadata = video_processing.process_video_upload(video_file)
        
        # Create video record
        video = Video(
            user_id=1,  # Hardcoded for testing
            title=request.form.get('title', 'Untitled'),
            description=request.form.get('description', ''),
            filename=video_metadata['storage_filename'],
            original_filename=video_metadata['original_filename'],
            status='pending'
        )
        
        db.session.add(video)
        db.session.commit()
        
        return jsonify({
            'message': 'Video upload successful',
            'video_id': video.id,
            'status': 'pending'
        }), 202
        
    except Exception as e:
        print(f"Upload error: {str(e)}")  # For debugging
        return jsonify({'error': str(e)}), 500