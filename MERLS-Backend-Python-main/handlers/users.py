import logging
from flask import Blueprint, request, jsonify

users_bp = Blueprint('users_bp', __name__)
logger = logging.getLogger(__name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    from repositories.participants_repo import ParticipantsRepo
    participant_repo = ParticipantsRepo()

    try:
        participant_id = request.args.get('participant_id')
        participant_name = request.args.get('participant_name')
        users = participant_repo.search(
            participant_id=participant_id,
            participant_name=participant_name,
        )
        return jsonify(users)

    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({"error": "Internal server error"}), 500
