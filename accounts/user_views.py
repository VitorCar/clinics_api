from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import CustomUsuario
from .serializers import UserSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retornar todos os usuários e seus dados',
        responses={200: UserSerializer},
        tags=['Usuários']
    ),
    post=extend_schema(
        description='Criar usuário',
        request=UserSerializer,
        responses={201: UserSerializer},
        tags=['Usuários']
    )
)
class UserListCreateApiView(ListCreateAPIView):

    queryset = CustomUsuario.objects.all()
    permission_classes = (AllowAny,) # momentanio 
    serializer_class = UserSerializer


@extend_schema_view(
    get=extend_schema(
        description='Retorna os dados de um usuário específico',
        responses={200: UserSerializer},
        tags=['Usuários']
    ),
    put=extend_schema(
        description='Atualiza todos os dados de um usuário',
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=['Usuários']
    ),
    patch=extend_schema(
        description='Atualiza parcialmente os dados de um usuário',
        request=UserSerializer,
        responses={200: UserSerializer},
        tags=['Usuários']
    ),
    delete=extend_schema(
        description='Remove um usuário do sistema',
        responses={204: None},
        tags=['Usuários']
    )
)
class UserRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):

    queryset = CustomUsuario.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
