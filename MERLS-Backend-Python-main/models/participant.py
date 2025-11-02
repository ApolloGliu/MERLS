class Participant:
    def __init__(self, participant_id="", participant_name="", is_completed_en=False,
                 is_completed_cn=False, is_active=False):
        self.participant_id = participant_id
        self.participant_name = participant_name
        self.is_completed_en = is_completed_en
        self.is_completed_cn = is_completed_cn
        self.is_active = is_active
