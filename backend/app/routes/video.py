# app/routes/video.py
from flask import Blueprint, request, current_app, jsonify
from werkzeug.utils import secure_filename
from ..services.video_processing import VideoProcessingService
from ..models.video import Video
from ..middleware.auth import require_auth
import logging

video_bp = Blueprint('video', __name__)
logger = logging.getLogger(__name__)

# Configure maximum file size (100MB)
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB in bytes

@video_bp.route('/upload', methods=['POST'])
@require_auth
async def upload_video():
    """
    Handle video upload with chunked streaming support
    """
    try:
        # Validate request has the file
        if 'video' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        video_file = request.files['video']
        if not video_file.filename:
            return jsonify({'error': 'No selected file'}), 400

        # Check file size
        if request.content_length > MAX_CONTENT_LENGTH:
            return jsonify({'error': 'File too large. Maximum size is 100MB'}), 413

        # Process the video upload
        video_processing = VideoProcessingService()
        video_metadata = await video_processing.process_video_upload(video_file)

        # Create video record in database
        video = Video(
            user_id=request.user.id,  # From auth middleware
            title=request.form.get('title', 'Untitled'),
            description=request.form.get('description', ''),
            filename=video_metadata['storage_filename'],
            status=video_metadata['status'],
            original_filename=video_metadata['original_filename']
        )
        video.save()

        return jsonify({
            'message': 'Video upload successful',
            'video_id': video.id,
            'status': 'processing'
        }), 202

    except ValueError as e:
        logger.warning(f"Invalid upload attempt: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Add Video model if not exists
@video_bp.route('/videos/<int:video_id>', methods=['GET'])
@require_auth
def get_video(video_id):
    """Get video details and processing status"""
    video = Video.query.get_or_404(video_id)
    
    # Check if user has access to this video
    if video.user_id != request.user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'status': video.status,
        'created_at': video.created_at.isoformat(),
        'urls': video.get_urls()  # We'll implement this later with CDN URLs
    })