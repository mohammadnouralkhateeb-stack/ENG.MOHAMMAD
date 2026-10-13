from crewai import LLM
from django.conf import settings

basic_llm = LLM(
    model=settings.LLM_MODEL,
    temperature=settings.LLM_DEFAULT_TEMPERATURE,
    api_key=settings.LLM_API_KEY,
    base_url=settings.LLM_BASE_URL,
)
