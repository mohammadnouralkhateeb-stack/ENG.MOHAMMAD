from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from core.crews.tools import basic_llm

@CrewBase
class SearchAgentCrew():
    """Search Agent Crew"""

    agents_config = 'agent.yaml'
    tasks_config = 'task.yaml'

    @agent
    def job_search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['job_search_agent'],
            llm=basic_llm,
            verbose=True,
        )

    @task
    def search_matching_jobs_task(self) -> Task:
        return Task(
            config=self.tasks_config['search_matching_jobs_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Job Search crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )