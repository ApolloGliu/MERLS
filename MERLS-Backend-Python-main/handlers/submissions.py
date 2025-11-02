from flask import Blueprint, request, jsonify
import logging

submissions_bp = Blueprint('submissions_bp', __name__)
logger = logging.getLogger(__name__)

@submissions_bp.route('/submissions', methods=['POST'])
def handle_submission():
    # Import inside the function to prevent circular imports
    from repositories.submissions_repo import SubmissionsRepo
    from repositories.participants_repo import ParticipantsRepo
    from models.submission import Submission

    try:
        data = request.json
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        participant_id = data.get('participantId')
        if not participant_id:
            return jsonify({"error": "Missing participantId"}), 400

        participant_repo = ParticipantsRepo()
        participant = participant_repo.get_by_id(participant_id)
        if not participant or not participant.get('is_active', False):
            return jsonify({"error": "Participant not found or inactive"}), 404

        submission = Submission(
            participant_id=participant_id,
            user_ans=data.get('userAns', {}),
            is_en=data.get('isEN', False),
            is_audio_test=data.get('isAudioTest', False),
            audio_submission_list=data.get('audioSubmissionList', {}),
            submission_type=data.get('submissionType'),
            story_submission_list=data.get('storySubmissionList', {}),
            retell_submission_list=data.get('retellSubmissionList', {})
        )

        if submission.submission_type:
            lang = 'EN' if submission.is_en else 'CN'
            participant_repo.set_completed_flag(participant_id, submission.submission_type, lang)

        submissions_repo = SubmissionsRepo()

        if submission.user_ans:
            submissions_repo.insert_answers_batch(
                participant_id=submission.participant_id,
                is_en=submission.is_en,
                answers=submission.user_ans,
            )

        for qid, url in submission.audio_submission_list.items():
            submissions_repo.insert_audio_submission(
                participant_id=submission.participant_id,
                question_id=int(qid),
                audio_url=url,
                is_en=submission.is_en,
            )

        for qid, story_data in submission.story_submission_list.items():
            submissions_repo.insert_story_submission(
                participant_id=submission.participant_id,
                question_id=int(qid),
                story_id=story_data.get('storyId'),
                audio_url=story_data.get('audioUrl'),
                is_en=submission.is_en,
                answer_transcript=story_data.get('transcript'),
            )

        for qid, retell_data in submission.retell_submission_list.items():
            submissions_repo.insert_retell_submission(
                participant_id=submission.participant_id,
                question_id=int(qid),
                story_id=retell_data.get('storyId'),
                audio_url=retell_data.get('audioUrl'),
                is_en=submission.is_en,
                answer_transcript=retell_data.get('transcript'),
            )

        return jsonify({"message": "Submission saved successfully"}), 201

    except Exception as e:
        logger.error(f"Error handling submission: {e}")
        return jsonify({"error": "Internal server error"}), 500
