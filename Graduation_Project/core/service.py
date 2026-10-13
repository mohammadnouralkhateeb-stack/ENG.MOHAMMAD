import json

from crewai_tools import SerperDevTool
from core.crews.read_cv_agent.crew import ReadCvAgentCrew
from core.crews.search_agent.crew import SearchAgentCrew
from pypdf import PdfReader


def _search_job_listings(job_title, location, technical_skills):
    skills = ", ".join(technical_skills)
    query = f"{job_title} jobs in {location}"
    if skills:
        query = f"{query} requiring {skills}"
    return SerperDevTool().run(search_query=query)


def _parse_crew_output(output):
    if isinstance(output, (dict, list)):
        return output

    json_dict = getattr(output, "json_dict", None)
    if json_dict is not None:
        return json_dict

    pydantic_output = getattr(output, "pydantic", None)
    if pydantic_output is not None:
        return pydantic_output.model_dump()

    raw_output = getattr(output, "raw", output)
    if not isinstance(raw_output, str):
        raise TypeError("Crew output must be JSON text or structured JSON data.")
    return json.loads(raw_output)


def run_pipeline(resume_file, job_details):
    resume_file.seek(0)
    reader = PdfReader(resume_file)
    extracted_text = "\n".join(
        text
        for page in reader.pages
        if (text := page.extract_text())
    )

    resume_crew = ReadCvAgentCrew()
    resume_output = resume_crew.crew().kickoff(
        inputs={"extracted_text": extracted_text}
    )
    resume_data = _parse_crew_output(resume_output)
    if not isinstance(resume_data, dict):
        raise ValueError("Resume analysis must return a JSON object.")

    technical_skills = resume_data.get("technical_skills")
    if not isinstance(technical_skills, list) or not all(
        isinstance(skill, str) for skill in technical_skills
    ):
        raise ValueError("Resume analysis must include a list of technical skills.")

    job_title = job_details["job_title"]
    location = job_details["location"]
    search_results = _search_job_listings(
        job_title,
        location,
        technical_skills,
    )

    search_crew = SearchAgentCrew()
    search_output = search_crew.crew().kickoff(
        inputs={
            "technical_skills": technical_skills,
            "job_title": job_title,
            "location": location,
            "search_results": search_results,
        }
    )
    search_results = _parse_crew_output(search_output)
    if not isinstance(search_results, list):
        raise ValueError("Job search must return a JSON list.")
    return search_results