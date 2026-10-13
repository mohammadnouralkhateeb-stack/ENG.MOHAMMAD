from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from core.crews.tools import basic_llm

@CrewBase
class ReadCvAgentCrew():
    """Read Cv Agent Crew"""

    agents_config = 'agent.yaml'
    tasks_config = 'task.yaml'

    @agent
    def resume_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_analyzer_agent'],
            llm=basic_llm,
            verbose=True
        )

    @task
    def extract_resume_skills_task(self) -> Task:
        return Task(
            config=self.tasks_config['extract_resume_skills_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ReadCvAgent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )