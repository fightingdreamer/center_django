from rest_framework import serializers

from link_shortener import mapping, models


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Redirection
        fields = ["id", "user_ip", "user_agent"]


class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Redirection
        fields = ["id", "hits"]


class LocationSerializer(serializers.Serializer):
    location = serializers.URLField(max_length=1023, allow_blank=False)


class RedirectionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("get_name")

    def get_name(self, obj):
        return mapping.encode_with_padding(obj.id, size=9, randomize=False)

    class Meta:
        model = models.Redirection
        fields = ["name"]
