from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel
from typing import List


# 1. تعريف الـ Schema للمخرجات المضمونة
class ScreeningReportSchema(BaseModel):
    score: float
    strengths: List[str]
    missing_skills: List[str]
    recommendation: str
    summary: str


@CrewBase
class ResumeScreeningCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def resume_screening_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_screening_agent"],
            verbose=True,
        )

    @task
    def resume_screening_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_screening_task"],
            output_json=ScreeningReportSchema,  # إجبار النموذج على إرجاع هذا الهيكل
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )