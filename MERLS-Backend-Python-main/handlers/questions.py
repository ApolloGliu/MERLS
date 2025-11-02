# handlers/questions.py
from flask import Blueprint, request, jsonify

questions_bp = Blueprint('questions_bp', __name__)

@questions_bp.route('/questions', methods=['GET'])
def get_questions():
    from repositories.questions_repo import QuestionsRepo
    repo = QuestionsRepo()

    lang = request.args.get('language')
    test_type = request.args.get('type')
    story_id = request.args.get('story_id', type=int)

    if lang not in ('CN', 'EN'):
        return jsonify({'error': 'Language must be CN or EN'}), 400
    if test_type not in ('repetition', 'matching', 'story'):
        return jsonify({'error': 'Type must be repetition, matching, or story'}), 400

    try:
        data = repo.get_questions(test_type=test_type, lang=lang, story_id=story_id)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
