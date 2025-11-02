class Submission:
    """
    Data model for a participant submission.
    """
    def __init__(self, participant_id, user_ans=None, is_en=False, is_audio_test=False,
                 audio_submission_list=None, submission_type=None,
                 story_submission_list=None, retell_submission_list=None):
        self.participant_id = participant_id
        self.user_ans = user_ans or {}
        self.is_en = is_en
        self.is_audio_test = is_audio_test
        self.audio_submission_list = audio_submission_list or {}
        self.submission_type = submission_type
        self.story_submission_list = story_submission_list or {}
        self.retell_submission_list = retell_submission_list or {}

