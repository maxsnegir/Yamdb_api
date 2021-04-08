from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class JWTSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=24, min_length=24)

    def validate(self, data):
        user = get_object_or_404(User, email=data['email'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': "Неверный код подтверждения"})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'email',
                  'role']
