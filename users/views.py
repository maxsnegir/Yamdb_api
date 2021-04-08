from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAdmin
from users.serializers import EmailSerializer, JWTSerializer, UserSerializer
from users.utils import get_token_for_user, send_email
import uuid

User = get_user_model()


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.get_or_create(email=serializer.data['email'],
                                      defaults={'username': uuid.uuid4(),
                                                'email': serializer.data[
                                                    'email']})
    user = user[0]
    user.confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_email(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = JWTSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, email=serializer.data['email'])
    return Response(get_token_for_user(user), status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete', ]

    @action(methods=['get', 'patch'], permission_classes=[IsAuthenticated, ],
            detail=False)
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
