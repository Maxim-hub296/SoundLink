from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Song
from .serializers import SongSerializer
from .utils import extract_audio_metadata, delete_audio_file


# Create your views here.
class SongUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            song = serializer.save(user=request.user)

            metadata = extract_audio_metadata(song.file.path)

            if not song.title and metadata['title']:
                song.title = metadata['title']
            if not song.artist and metadata['artist']:
                song.artist = metadata['artist']
            if not song.length and metadata['length']:
                song.length = metadata['length']

            song.save()
            return Response(SongSerializer(song).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        songs = Song.objects.filter(user=request.user)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


class SongDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        song = Song.objects.get(user=request.user, id=request.data['id'])
        file_path = song.file.path
        song.delete()
        ok = delete_audio_file(file_path)
        if not ok:
            return Response({"error": "File not deleted"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
