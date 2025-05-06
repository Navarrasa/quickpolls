from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Poll, Option, Category, CustomUser, Vote, Flag
from better_profanity import profanity

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):

    """
    CustomUserSerializer -> Serializador para o modelo CustomUser.
    Utilizado para criar novos usuários e validar os dados de entrada.
    """

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    # Verifica no processo de registro de um novo usuário se o campo username já existe no Banco de Dados
    # Caso exista, retorna erro ao usuário de que o apelido já está em uso.
    # Caso não exista, cria um novo usuário.
    def validate_username(self, value):
        if value: 
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


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("É obrigatório ter um título em sua votação!")
        if profanity.contains_profanity(value):
            raise serializers.ValidationError("O título contém linguagem imprópria.")
        return value

    def validate_description(self, value):
        if profanity.contains_profanity(value):
            raise serializers.ValidationError("A descrição contém linguagem imprópria.")
        return value

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("A data de término deve ser posterior à data de início.")
        return data


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'
    
    def validate_text(self, text):
        if not text:
            raise serializers.ValidationError("É obrigatório que as opções tenham um texto!")
        return text
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    def validate_name(self, name):
        if not name:
            raise serializers.ValidationError("Cada categoria deve conter um nome!")
        return name


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
    
    