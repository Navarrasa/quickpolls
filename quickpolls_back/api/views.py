from rest_framework import generics
from .serializer import CustomUserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterView(generics.CreateAPIView):

    """
    View para registrar um novo usuário.
    queryset -> Define o conjunto de dados que será manipulado pela view.
    serializer_class -> Define o serializer que será utilizado para validar e serializar os dados.

    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

