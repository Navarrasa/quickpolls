from rest_framework import generics
from .serializer import CustomUserSerializer
from django.contrib.auth import get_user_model

# from django.contrib.auth import get_user_model -> Importa a função get_user_model do Django, que retorna o modelo de usuário ativo.
# Isso é útil para garantir que você esteja usando o modelo de usuário correto, especialmente se você estiver usando um modelo de usuário personalizado.
# nesse caso, estou utilizando um modelo customizado de usuário.
User = get_user_model()

# RegisterView -> Classe que herda de generics.CreateAPIView, que é uma view genérica do Django Rest Framework para criar novos objetos.
# A classe fornece uma implementação padrão para o método POST, que é usado para criar novos objetos.
# O método POST é utilizado para enviar dados ao servidor, e a view irá criar um novo usuário com os dados fornecidos no corpo da requisição.
class RegisterView(generics.CreateAPIView):

    """
    View para registrar um novo usuário.
    queryset -> Define o conjunto de dados que será manipulado pela view.
    serializer_class -> Define o serializer que será utilizado para validar e serializar os dados.

    """

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

