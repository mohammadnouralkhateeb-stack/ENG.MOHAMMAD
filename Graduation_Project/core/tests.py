from django.conf import settings
from django.contrib.auth.models import User as AuthUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase, override_settings
from rest_framework.authtoken.models import Token
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from core.crews.read_cv_agent.crew import ReadCvAgentCrew
from core.crews.search_agent.crew import SearchAgentCrew
from core.models import SearchHistory, User as CoreUser
from core.serializers.resume_serializer import ResumeSerializer
from core.service import _search_job_listings
from core.crews.tools import basic_llm
from pypdf import PdfWriter


def create_pdf(page_count):
    writer = PdfWriter()
    for _ in range(page_count):
        writer.add_blank_page(width=72, height=72)
    pdf_file = BytesIO()
    writer.write(pdf_file)
    return pdf_file.getvalue()


class LLMConfigurationTests(SimpleTestCase):
    def test_shared_llm_uses_configured_provider_settings(self):
        self.assertEqual(basic_llm.model, settings.LLM_MODEL)
        self.assertEqual(basic_llm.api_key, settings.LLM_API_KEY)
        self.assertEqual(basic_llm.base_url, settings.LLM_BASE_URL)
        self.assertEqual(basic_llm.additional_params["tool_choice"], "auto")
        completion_params = basic_llm._prepare_completion_params(
            [{"role": "user", "content": "Return the result."}],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "Answer",
                        "parameters": {"type": "object", "properties": {}},
                    },
                }
            ],
        )
        self.assertEqual(completion_params["tool_choice"], "auto")

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


class SearchHistoryTests(TestCase):
    def test_login_returns_the_users_previous_search_results(self):
        user = AuthUser.objects.create_user(username="history-user", password="secret")
        SearchHistory.objects.create(
            user=user,
            job_title="Python Developer",
            location="Irbid",
            description="Build backend services",
            score=85,
            link="https://example.com/jobs/python",
        )

        response = self.client.post(
            "/user/",
            {"username": "history-user", "password": "secret"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "history_found")
        self.assertEqual(response.data["user_id"], user.id)
        self.assertTrue(response.data["token"])
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["job_title"], "Python Developer")

    @patch("core.views.save_details_view.run_pipeline")
    def test_completed_search_is_added_to_users_history(self, run_pipeline):
        run_pipeline.return_value = [
            {
                "job_title": "Python Developer",
                "company": "Example Co",
                "location": "Irbid",
                "description": "Build backend services",
                "score": 85,
                "link": "https://example.com/jobs/python",
            }
        ]
        user = AuthUser.objects.create_user(username="search-user", password="secret")
        token = Token.objects.create(user=user)

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    "/details/",
                    {
                        "job_title": "Python Developer",
                        "location": "Irbid",
                        "description": "Build backend services",
                        "salary": "500",
                        "resume_file": SimpleUploadedFile(
                            "resume.pdf", create_pdf(1), content_type="application/pdf"
                        ),
                    },
                    HTTP_AUTHORIZATION=f"Token {token.key}",
                )

        self.assertEqual(response.status_code, 201, response.data)
        history_record = SearchHistory.objects.get(user=user)
        self.assertEqual(history_record.job_title, "Python Developer")
        self.assertEqual(history_record.score, 85)
        self.assertTrue(CoreUser.objects.filter(user_name="search-user").exists())


class ResumeUploadValidationTests(TestCase):
    def setUp(self):
        self.user = CoreUser.objects.create(user_name="resume-user", password="secret")

    def validate_upload(self, file_name, contents):
        return ResumeSerializer(
            data={
                "user": self.user.pk,
                "resume_file": SimpleUploadedFile(
                    file_name, contents, content_type="application/pdf"
                ),
            }
        ).is_valid()

    def test_accepts_pdf_with_twenty_pages(self):
        serializer = ResumeSerializer(
            data={
                "user": self.user.pk,
                "resume_file": SimpleUploadedFile(
                    "resume.pdf", create_pdf(20), content_type="application/pdf"
                ),
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_rejects_pdf_with_more_than_twenty_pages(self):
        self.assertFalse(self.validate_upload("resume.pdf", create_pdf(21)))

    def test_rejects_non_pdf_file(self):
        self.assertFalse(self.validate_upload("resume.docx", b"not a PDF"))

    def test_rejects_invalid_pdf_content(self):
        self.assertFalse(self.validate_upload("resume.pdf", b"not a PDF"))
