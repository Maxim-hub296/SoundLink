from rest_framework import serializers

from .models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'length', 'file', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
