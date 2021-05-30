from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, serializers, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room


# Django Views

def hello(request):
    return HttpResponse("<h1>hello</h1>")

# Django REST Framework

class ListRoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # If the user does not have a session, create a session
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # Get data from request & serializer
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            # Update the room if the host already owns a room, else Create new room
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()

            # Return a response of the record created
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        # Error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)