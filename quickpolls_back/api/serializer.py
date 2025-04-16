from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):

    """
    CustomUserSerializer -> Serializador para o modelo CustomUser.
    Utilizado para criar novos usuários e validar os dados de entrada.
    """

    class Meta:
        # Define o modelo a ser utilizado e os campos que serão serializados.
        # O campo 'password' é definido como write_only, o que significa que ele não será incluído na representação serializada do usuário.
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # Verifica no processo de registro de um novo usuário se o campo username já existe no Banco de Dados
    # Caso exista, retorna erro ao usuário de que o apelido já está em uso.
    # Caso não exista, cria um novo usuário.
    def validate_username(self, value):
        if value:  # Verifica unicidade apenas se o username for fornecido
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError('Este apelido já está em uso.')
        return value
    
    # Sobrescreve o método create para criar um novo usuário com a senha criptografada.
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username'),  # Pode ser None
            password=validated_data['password']
        )
        return user