from pypdf import PdfReader
from pypdf.errors import PdfReadError
from rest_framework import serializers

from core.models.resume import Resume


MAX_RESUME_PAGES = 20


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = "__all__"

    def validate_resume_file(self, uploaded_file):
        if not uploaded_file.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Only PDF files are allowed.")

        uploaded_file.seek(0)
        try:
            page_count = len(PdfReader(uploaded_file, strict=True).pages)
        except PdfReadError as exc:
            raise serializers.ValidationError(
                "The uploaded file must be a valid PDF."
            ) from exc
        finally:
            uploaded_file.seek(0)

        if page_count > MAX_RESUME_PAGES:
            raise serializers.ValidationError(
                f"The PDF must not exceed {MAX_RESUME_PAGES} pages."
            )

        return uploaded_file