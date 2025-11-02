from SupabaseClient import supabase

class ParticipantDB:

    @staticmethod
    def participant_if_valid(participant_id: str) -> bool:
        response = supabase.table('participants').select('participant_id').eq('participant_id', participant_id).execute()
        return len(response.data) > 0 if response.status_code == 200 else False

    @staticmethod
    def update_completed(participant_id: str, test_type: str, lang: str):
        column_map = {
            'story': {'cn': 'completed_story_cn', 'en': 'completed_story_en'},
            'repetition': {'cn': 'completed_repetition_cn', 'en': 'completed_repetition_en'},
            'matching': {'cn': 'completed_matching_cn', 'en': 'completed_matching_en'}
        }
        lang_code = 'en' if lang.lower() == 'en' else 'cn'
        column = column_map.get(test_type, {}).get(lang_code)
        if column:
            supabase.table('participants').update({column: True}).eq('participant_id', participant_id).execute()

# This method checks if a participane exists but does not check if they are active or not

# Ony flags known test types and languages–does nothing if unknown test type or language is passes

# Maybe we can add code to return success or failure indicators from update methods
