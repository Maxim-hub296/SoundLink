from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Playlist
from .serializers import PlaylistSerializer


class PlaylistCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = PlaylistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PlaylistsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        playlists = Playlist.objects.filter(user=request.user)
        serializer = PlaylistSerializer(playlists, many=True)
        return Response(serializer.data)


class PlaylistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        playlist = Playlist.objects.get(id=pk)
        serializer = PlaylistSerializer(playlist)
        return Response(serializer.data)


class PlaylistDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        playlist = Playlist.objects.get(id=pk)
        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
