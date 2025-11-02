from typing import Any, Dict, List, Optional
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

class QuestionsRepo:
    def __init__(self) -> None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY. Check .env.")
        self.client = create_client(url, key)

    @staticmethod
    def _resolve_table(test_type: str, lang: str) -> str:
        t = (test_type or "").lower()
        l = (lang or "").upper()

        if t == "matching":
            return "chinese_questions" if l == "CN" else "english_questions"
        if t == "repetition":
            return "chinese_repetition" if l == "CN" else "english_repetition"
        if t == "story":
            return "story_questions"

        raise ValueError(f"Unsupported test_type: {test_type}")

    def get_questions(
        self,
        *,
        test_type: str,
        lang: str,
        story_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        table = self._resolve_table(test_type, lang)

        q = self.client.table(table).select("*").eq("is_active", True)
        if test_type.lower() == "story" and story_id is not None:
            q = q.eq("story_id", story_id)
        if limit:
            q = q.limit(limit)

        res = q.order("question_id").execute()
        if not res or getattr(res, "error", None):
            raise RuntimeError(f"Supabase error: {getattr(res, 'error', 'unknown error')}")
        return res.data or []

    def list_stories(self) -> List[Dict[str, Any]]:
        res = (
            self.client.table("story_test")
            .select("*")
            .eq("is_active", True)
            .order("story_id")
            .execute()
        )
        if not res or getattr(res, "error", None):
            raise RuntimeError(f"Supabase error: {getattr(res, 'error', 'unknown error')}")
        return res.data or []
