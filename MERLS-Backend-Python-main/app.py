from flask import Flask, jsonify
import logging
import werkzeug.exceptions

# Import Blueprints
from handlers.audio_upload import audio_bp
from handlers.export import export_bp
from handlers.questions import questions_bp
from handlers.submissions import submissions_bp
from handlers.users import users_bp

# Create Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(audio_bp)
app.register_blueprint(export_bp)
app.register_blueprint(questions_bp)
app.register_blueprint(submissions_bp)
app.register_blueprint(users_bp)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# Error handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad Request", "message": str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": str(e)}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed", "message": str(e)}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500

@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_http_exception(e):
    return jsonify({"error": e.name, "message": e.description}), e.code

# Root route (for testing)
@app.route("/")
def index():
    return jsonify({"message": "MERLS backend running!"})

