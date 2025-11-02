from flask import Blueprint, request, jsonify
import boto3
import base64

audio_bp = Blueprint('audio_bp', __name__)

@audio_bp.route('/audio-upload', methods=['POST'])
def upload_audio():
    data = request.json
    audio_bytes = base64.b64decode(data['audioData'])
    user_id = data['userId']
    question_id = str(data['questionId'])
    file_type = data['fileType']
    bucket_name = data['bucketName']
    key = f"{user_id}/question_{question_id}.webm"

    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=key, Body=audio_bytes, ContentType=file_type)

    return jsonify({"message": "Upload successful", "key": key}), 200
