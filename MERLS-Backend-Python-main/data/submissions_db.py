from SupabaseClient import supabase

class SubmissionsDB:

    @staticmethod
    def post_submissions_to_db(submission):
        # Only handling user_ans dictionary for matching/multiple choice and repetition text
        if not submission.is_audio_test and submission.user_ans:
            for question_id, user_answer in submission.user_ans.items():
                supabase.table('submissions').insert({
                    'participant_id': submission.participant_id,
                    'question_id': question_id,
                    'answer': user_answer,
                    'is_en': submission.is_en
                }).execute()
        # For audio, story, retell submission lists, expand as needed:
        if submission.is_audio_test and submission.audio_submission_list:
            for question_id, audio_link in submission.audio_submission_list.items():
                supabase.table('submissions').insert({
                    'participant_id': submission.participant_id,
                    'question_id': question_id,
                    'audio_url': audio_link,
                    'is_en': submission.is_en
                }).execute()
        if submission.story_submission_list:
            for question_id, story_answer in submission.story_submission_list.items():
                supabase.table('submissions').insert({
                    'participant_id': submission.participant_id,
                    'question_id': question_id,
                    'story_answer': story_answer,
                    'is_en': submission.is_en
                }).execute()
        if submission.retell_submission_list:
            for question_id, retell_answer in submission.retell_submission_list.items():
                supabase.table('submissions').insert({
                    'participant_id': submission.participant_id,
                    'question_id': question_id,
                    'retell_answer': retell_answer,
                    'is_en': submission.is_en
                }).execute()

# This method needs to be able to process more attributes if the application handles more submission types. Maybe audio_submission_list, story_submission_list, or retell_submission_list
