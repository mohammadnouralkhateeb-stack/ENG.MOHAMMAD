from crewai.flow import Flow, listen, start
from core.crews.interview_questions_agent.crew import InterviewQuestionCrew
from core.crews.screening_result_agent.crew import ResumeScreeningCrew
from .schema import HRPipelineState


class HRPipelineFlow(Flow[HRPipelineState]):

    @start()
    async def screen_resume(self): # async , await : يعني السماح للبرنامج بان يستمر حتى اثناء عمل الدالة
        result = await ResumeScreeningCrew().crew().kickoff_async( # هون بتم استدعاء النموذج و حقنه بالمعلومات
            inputs={
                "candidate_resume": self.state.candidate_resume, 
                "job_title": self.state.job_title,
                "job_description": self.state.job_description,
                "required_skills": self.state.required_skills,
            }
        )
        # result.pydantic أو result.json_dict يرجّع dict جاهز ومضمون
        self.state.screening_output = result.pydantic.model_dump()
        return self.state.screening_output

    @listen(screen_resume)
    async def generate_questions(self):
        result = await InterviewQuestionCrew().crew().kickoff_async(
            inputs={
                "candidate_resume": self.state.candidate_resume,
                "job_title": self.state.job_title,
                "job_description": self.state.job_description,
                "screening_report": str(self.state.screening_output),
            }
        )
        self.state.interview_output = result.pydantic.model_dump()
        
        # إعداد النتيجة النهائية المجمّعة في نفس الخطوة دون دالة ثالثة
        self.state.final_output = {
            "screening_report": self.state.screening_output,
            "interview_questions": self.state.interview_output,
        }
        return self.state.final_output