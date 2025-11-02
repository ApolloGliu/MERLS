# MERLS-Backend-Python






data/participant_db.py
  - Checks if a participant exists in the database.
  - Updates participant completion status fields depending on test type and language.
Possible improvements:
  - Add docstrings explaining methods with parameters and return types.
  - Add error handling to catch and log failures in database calls.
  - Validate inputs for test_type and lang with warnings or errors on invalid values.
  - Optionally return success/failure status for the update method to handle downstream logic.


data/audio_uploads.py
  - Accepts a POST request with base64-encoded audio and metadata.
  - Decodes audio and uploads it to specified AWS S3 bucket.
  - Returns success message and the storage key.
Possible improvements:
  - Add docstring for the route explaining expected JSON fields.
  - Add try-except around S3 operations to handle and log errors gracefully.
  - Validate required request fields and file types.
  - Control or restrict bucket_name server-side for security.
  - Consider limits on file size and appropriate error responses.


handlers/export.py
  - On GET, fetches submissions from PostgreSQL filtered by participant and language.
  - Converts results to an in-memory Excel file and sends it as a downloadable response.
Possible improvements:
  - Add docstring describing endpoint and parameters.
  - Add error handling for DB connection failures, missing parameters, and empty queries.
  - Validate language parameter and return meaningful errors on invalid input.
  - Consider using connection pooling.
  - Add authentication/authorization to protect data.


handlers/questions.py
  - API GET endpoint that returns test questions filtered by language (CN or EN) and test type (story, matching, repetition).
  - Selects from corresponding Supabase tables and returns active questions.
Possible improvements:
  - Add comprehensive docstring with parameter and return info.
  - Validate query params fully, handle missing params explicitly.
  - Add pagination support to limit large responses.
  - Add internal logging for failed database calls.



handlers/submissions.py
  - Accepts JSON submission data.
  - Validates that participant exists.
  - Updates participant's completion flags depending on submission type and language.
  - Inserts user answers into the submissions table.
Possible improvements:
  - Add detailed docstring for expected JSON structure.
  - Add input validation for required fields.
  - Add try-except with error logging for DB operations.
  - Handle audio / story / retell submission data beyond user answers.
  - Wrap inserts in transactions for atomicity.


handlers/users.py
  - GET endpoint to retrieve active participants with optional filters by ID or name.
Possible improvements:
  - Add docstring describing filters and response.
  - Validate query parameters.
  - Add pagination support.
  - Add authentication and rights management.
  - Log errors and exceptions.


models/audio_uploads.py
  - Defines a container class for audio upload requests.
  - Provides a representation method that masks audio data.
Possible improvements:
  - Add detailed class and method docstrings.
  - Consider adding validation or data conversion methods.


models/participant.py
  - Represents a participant with ID, name, language completion status, and active flag.
Possible improvements:
  - Add comprehensive class docstring.
  - Add type hints.
  - Potentially implement utility methods for status updates.


models/submissions.py
  - Models a test submission with multiple optional fields for various test types.
Possible improvements:
  - Add detailed class docstring.
  - Add validation or helper methods.
  - Use type hints.



