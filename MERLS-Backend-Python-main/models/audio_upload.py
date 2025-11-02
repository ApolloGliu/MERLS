class AudioUploadRequest:
    """
    Model for audio upload requests.
    """
    def __init__(self, file_name, file_type, audio_data, user_id, question_id, bucket_name):
        self.file_name = file_name
        self.file_type = file_type
        self.audio_data = audio_data
        self.user_id = user_id
        self.question_id = question_id
        self.bucket_name = bucket_name

    def __repr__(self):
        return (f"AudioUploadRequest{{bucketName={self.bucket_name}, fileName={self.file_name}, "
                f"fileType={self.file_type}, audioData={'[BASE64_DATA]' if self.audio_data else 'null'}}}")
