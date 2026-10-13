from django.conf import settings
from django.test import SimpleTestCase
from unittest.mock import patch

from core.crews.read_cv_agent.crew import ReadCvAgentCrew
from core.crews.search_agent.crew import SearchAgentCrew
from core.service import _search_job_listings
from core.crews.tools import basic_llm


class LLMConfigurationTests(SimpleTestCase):
    def test_shared_llm_uses_configured_provider_settings(self):
        self.assertEqual(basic_llm.model, settings.LLM_MODEL)
        self.assertEqual(basic_llm.api_key, settings.LLM_API_KEY)
        self.assertEqual(basic_llm.base_url, settings.LLM_BASE_URL)

    def test_both_crews_use_the_shared_llm(self):
        crews = [ReadCvAgentCrew().crew(), SearchAgentCrew().crew()]

        for crew_instance in crews:
            self.assertTrue(crew_instance.agents)
            for agent_instance in crew_instance.agents:
                self.assertIs(agent_instance.llm, basic_llm)

    @patch("core.service.SerperDevTool")
    def test_job_listings_are_searched_directly(self, serper_tool):
        serper_tool.return_value.run.return_value = "search results"

        results = _search_job_listings(
            "Python Developer",
            "Irbid",
            ["Django", "PostgreSQL"],
        )

        self.assertEqual(results, "search results")
        serper_tool.return_value.run.assert_called_once_with(
            search_query="Python Developer jobs in Irbid requiring Django, PostgreSQL"
        )

    def test_search_agent_does_not_call_tools(self):
        search_crew = SearchAgentCrew().crew()

        self.assertTrue(all(not agent.tools for agent in search_crew.agents))
