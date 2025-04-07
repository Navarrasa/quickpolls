from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Define email field with uniqueness validator
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    
    class Meta:
        model = get_user_model()  # Dynamically fetches the User model
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'password']  # Fields to serialize
        extra_kwargs = {
            'password': {'write_only': True},  # Password is write-only for security
            'first_name': {'required': False},  # First name is optional
            'last_name': {'required': False},   # Last name is optional
        }

    def create(self, validated_data):
        """
        Creates a new user instance with the provided validated data.

        Args:
            validated_data (dict): Validated user data from the request.

        Returns:
            User: The newly created user instance.

        Raises:
            serializers.ValidationError: If user creation fails due to unexpected errors.
        """
        try:
            # Create user with validated data using create_user for password hashing
            user = get_user_model().objects.create_user(
                **validated_data  # Unpack validated data directly
            )
            return user
        except Exception as e:
            # Handle any creation errors and return a meaningful message
            raise serializers.ValidationError(f"Erro ao criar usuário: {str(e)}")