from rest_framework import serializers

from core.models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = "__all__"
