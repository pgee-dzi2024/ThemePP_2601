from rest_framework import serializers


class MediaUploadSerializer(serializers.Serializer):
    media_file = serializers.FileField()
