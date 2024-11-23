# app/services/video_processing.py
from flask import current_app
import boto3
from botocore.exceptions import ClientError
import os
from werkzeug.utils import secure_filename
import uuid

class VideoProcessingService:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
            aws_secret_access_key=current_app.config['AWS_SECRET_KEY']
        )
        self.bucket_name = current_app.config['S3_BUCKET']
        self.allowed_extensions = {'mp4', 'mov', 'avi'}

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def generate_unique_filename(self, original_filename):
        ext = original_filename.rsplit('.', 1)[1].lower()
        return f"{str(uuid.uuid4())}.{ext}"

    def process_video_upload(self, file):
        """
        Process video upload:
        1. Validate file
        2. Generate unique filename
        3. Upload to S3
        4. Return metadata
        """
        if not file or not self.allowed_file(file.filename):
            raise ValueError("Invalid file type")

        try:
            filename = secure_filename(file.filename)
            unique_filename = self.generate_unique_filename(filename)
            
            # Upload original file to S3
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                f"uploads/original/{unique_filename}",
                ExtraArgs={'ContentType': file.content_type}
            )

            # Create video metadata record
            video_metadata = {
                'original_filename': filename,
                'storage_filename': unique_filename,
                'status': 'pending_transcoding',
                'versions': {
                    'original': f"uploads/original/{unique_filename}"
                }
            }

            return video_metadata

        except ClientError as e:
            current_app.logger.error(f"S3 upload error: {str(e)}")
            raise
        except Exception as e:
            current_app.logger.error(f"Video processing error: {str(e)}")
            raise