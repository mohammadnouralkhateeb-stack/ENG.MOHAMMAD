from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from typing import List


# 1. تعريف الـ Schema لأسئلة المقابلة
class InterviewQuestionsSchema(BaseModel):
    technical_questions: List[str]
    behavioral_questions: List[str]
    follow_up_questions: List[str]


@CrewBase
class InterviewQuestionCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def interview_question_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["interview_question_generator"],
            verbose=True,
        )

    @task
    def interview_question_task(self) -> Task:
        return Task(
            config=self.tasks_config["interview_question_task"],
            output_json=InterviewQuestionsSchema,  # إجبار النموذج على إرجاع الأسئلة كمصفوفات
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )