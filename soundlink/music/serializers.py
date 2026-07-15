from rest_framework import serializers

from .models import Song
from .utils import is_file_size_allowed, is_allowed_file_type


def validate_file_type(value):
    if is_allowed_file_type(value):
        return value
    raise serializers.ValidationError("Данный тип файла не поддерживается")


def validate_file_size(value):
    if is_file_size_allowed(value):
        return value
    raise serializers.ValidationError("Файл превышает допустимый размер")


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'length', 'file', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

    file = serializers.FileField(
        error_messages={"required": "Файл трека обязателен.", "invalid": "Некорректный файл."},
        validators=[validate_file_size, validate_file_type],
    )
