from rest_framework import serializers

from core.models.search_result import SearchResult


class SearchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult
        fields = "__all__"