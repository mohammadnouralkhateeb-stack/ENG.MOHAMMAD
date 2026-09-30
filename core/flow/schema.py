from typing import Dict, Optional

from pydantic import BaseModel


class HRPipelineState(BaseModel): # الفكرة منه هي تحديد انواع المتغيرات مسبقا مش اكثر
    """Shared state passed between steps of the HR pipeline flow."""

    # Identifiers — set when the flow loads its inputs from the database.
    candidate_id: Optional[int] = None
    job_position_id: Optional[int] = None

    # Inputs (supplied directly in "raw" mode, or loaded from the DB).
    candidate_resume: str = ""
    job_title: str = ""
    job_description: str = ""
    required_skills: str = ""

    # Outputs
    screening_output: Dict = {}
    interview_output: Optional[Dict] = None
    final_output: Dict = {}
