from rest_framework.response import Response
from rest_framework import status
from .serializer import UserRegistrationSerializer
from rest_framework.decorators import api_view

@api_view(['POST'])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)