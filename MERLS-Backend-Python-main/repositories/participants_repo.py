from typing import Any, Dict, List, Optional, Tuple
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY. Check your .env file.")

class ParticipantsRepo:
    TABLE = "participants"

    def __init__(self) -> None:
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def get_all(self) -> List[Dict[str, Any]]:
        res = self.client.table(self.TABLE).select("*").execute()
        if not res or getattr(res, "error", None):
            raise RuntimeError(f"get_all failed: {getattr(res, 'error', 'unknown error')}")
        return res.data or []

    def get_by_id(self, participant_id: str) -> Optional[Dict[str, Any]]:
        res = (
            self.client.table(self.TABLE)
            .select("*")
            .eq("participant_id", participant_id)
            .maybe_single()
            .execute()
        )
        if not res or getattr(res, "error", None) or not hasattr(res, "data"):
            return None
        return res.data

    def insert(self, participant_id: str, participant_name: Optional[str] = None) -> Dict[str, Any]:
        row = {
            "participant_id": participant_id,
            "participant_name": participant_name,
            "is_active": True,
            "completed_story_en": False,
            "completed_story_cn": False,
            "completed_matching_en": False,
            "completed_matching_cn": False,
            "completed_repetition_en": False,
            "completed_repetition_cn": False,
        }

        res = self.client.table(self.TABLE).insert(row).execute()
        if not res or getattr(res, "error", None):
            raise RuntimeError(f"insert failed: {getattr(res, 'error', 'unknown error')}")
        return (res.data or [{}])[0]

    def set_completed_flag(
        self, participant_id: str, test_type: str, lang: str, value: bool = True
    ) -> Tuple[int, List[Dict[str, Any]]]:
        test_type = test_type.lower()
        lang = lang.upper()

        column_map = {
            "story": {"CN": "completed_story_cn", "EN": "completed_story_en"},
            "matching": {"CN": "completed_matching_cn", "EN": "completed_matching_en"},
            "repetition": {"CN": "completed_repetition_cn", "EN": "completed_repetition_en"},
        }

        col = column_map.get(test_type, {}).get(lang)
        if not col:
            raise ValueError(f"Unsupported test_type/lang combination: {test_type}/{lang}")

        res = (
            self.client.table(self.TABLE)
            .update({col: value})
            .eq("participant_id", participant_id)
            .execute()
        )
        if not res or getattr(res, "error", None):
            raise RuntimeError(f"set_completed_flag failed: {getattr(res, 'error', 'unknown error')}")

        affected = len(res.data or [])
        return affected, (res.data or [])

    def search(
        self,
        participant_id: Optional[str] = None,
        participant_name: Optional[str] = None,
        only_active: bool = True,
    ) -> List[Dict[str, Any]]:
        q = self.client.table(self.TABLE).select("*")
        if only_active:
            q = q.eq("is_active", True)
        if participant_id:
            q = q.eq("participant_id", participant_id)
        if participant_name:
            q = q.eq("participant_name", participant_name)

        res = q.execute()
        if not res or getattr(res, "error", None):
            raise RuntimeError(f"search failed: {getattr(res, 'error', 'unknown error')}")
        return res.data or []
