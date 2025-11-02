from typing import Any, Dict, List, Optional
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY. Check your .env file.")

class SubmissionsRepo:
    TBL_SUBMISSIONS = "submissions"
    TBL_AUDIO = "audio_submissions"
    TBL_STORY = "story_submissions"
    TBL_RETELL = "retell_submissions"

    def __init__(self) -> None:
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def _ok(self, res: Any) -> List[Dict[str, Any]]:
        if not res or getattr(res, "error", None):
            raise RuntimeError(f"Supabase error: {getattr(res, 'error', 'unknown error')}")
        return res.data or []

    def insert_answer(self, participant_id: str, question_id: int, answer: int, is_en: bool, is_correct: Optional[bool] = None) -> Dict[str, Any]:
        row = {
            "participant_id": participant_id,
            "question_id": question_id,
            "answer": answer,
            "is_en": is_en,
        }
        if is_correct is not None:
            row["is_correct"] = is_correct
        res = self.client.table(self.TBL_SUBMISSIONS).insert(row).execute()
        data = self._ok(res)
        return data[0] if data else row

    def insert_answers_batch(self, participant_id: str, is_en: bool, answers: dict, with_correct: Optional[dict] = None) -> List[Dict[str, Any]]:
        rows = []
        for qid, ans in answers.items():
            row = {
                "participant_id": participant_id,
                "question_id": int(qid),
                "answer": int(ans),
                "is_en": is_en,
            }
            if with_correct and qid in with_correct:
                row["is_correct"] = bool(with_correct[qid])
            rows.append(row)
        if not rows:
            return []
        res = self.client.table(self.TBL_SUBMISSIONS).insert(rows).execute()
        return self._ok(res)

    def insert_audio_submission(self, participant_id: str, question_id: int, audio_url: str, is_en: bool, answer_transcript: Optional[str] = None, score: Optional[int] = None, question_transcript: Optional[str] = None) -> Dict[str, Any]:
        row = {
            "participant_id": participant_id,
            "question_id": question_id,
            "audio_url": audio_url,
            "is_en": is_en,
        }
        if answer_transcript is not None:
            row["answer_transcript"] = answer_transcript
        if question_transcript is not None:
            row["question_transcript"] = question_transcript
        if score is not None:
            row["score"] = score
        res = self.client.table(self.TBL_AUDIO).insert(row).execute()
        data = self._ok(res)
        return data[0] if data else row

    def insert_story_submission(self, participant_id: str, question_id: int, story_id: int, audio_url: str, is_en: bool, answer_transcript: Optional[str] = None, score: Optional[int] = None) -> Dict[str, Any]:
        row = {
            "participant_id": participant_id,
            "question_id": question_id,
            "story_id": story_id,
            "audio_url": audio_url,
            "is_en": is_en,
        }
        if answer_transcript is not None:
            row["answer_transcript"] = answer_transcript
        if score is not None:
            row["score"] = score
        res = self.client.table(self.TBL_STORY).insert(row).execute()
        data = self._ok(res)
        return data[0] if data else row

    def insert_retell_submission(self, participant_id: str, question_id: int, story_id: int, audio_url: str, is_en: bool, answer_transcript: Optional[str] = None, score: Optional[int] = None) -> Dict[str, Any]:
        row = {
            "participant_id": participant_id,
            "question_id": question_id,
            "story_id": story_id,
            "audio_url": audio_url,
            "is_en": is_en,
        }
        if answer_transcript is not None:
            row["answer_transcript"] = answer_transcript
        if score is not None:
            row["score"] = score
        res = self.client.table(self.TBL_RETELL).insert(row).execute()
        data = self._ok(res)
        return data[0] if data else row
