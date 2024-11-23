# app/routes/video.py
from flask import Blueprint, request, jsonify, current_app
from ..services.video_processing import VideoProcessingService
from ..models.video import Video
from app import db
import logging

video_bp = Blueprint('video', __name__)
logger = logging.getLogger(__name__)

@video_bp.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'status': 'Video routes working!'}), 200

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    logger.info('Upload endpoint called')
    try:
        if 'video' not in request.files:
            logger.warning('No video file in request')
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        if not video_file.filename:
            logger.warning('Empty filename')
            return jsonify({'error': 'No selected file'}), 400

        # Log successful file receipt
        logger.info('Received file: %s', video_file.filename)
            
        # Create video processing service
        video_processing = VideoProcessingService()
        
        # Process upload
        video_metadata = video_processing.process_video_upload(video_file)
        logger.info('Video processed: %s', video_metadata)
        
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
        logger.info('Video record created with ID: %s', video.id)
        
        return jsonify({
            'message': 'Video upload successful',
            'video_id': video.id,
            'status': 'pending'
        }), 202
        
    except Exception as e:
        logger.error('Upload error: %s', str(e), exc_info=True)
        return jsonify({'error': str(e)}), 500