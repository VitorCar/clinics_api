from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import CustomUsuario
from .forms import CustomUsuarioCreationForm, CustomUsuarioChangeForm, CustomSetPasswordForm
from .serializers import UserSerializer, UserListSerializer
from .utils import is_admin


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUsuario
    template_name = 'user_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10

    def test_func(self):
        return is_admin(self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_joined')
        q = self.request.GET.get('q')
        role_filter = self.request.GET.get('role')

        if q:
            queryset = queryset.filter(Q(full_name__icontains=q) | Q(email__icontains=q))
        if role_filter:
            queryset = queryset.filter(role=role_filter)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = CustomUsuario.Roles.choices
        return context


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CustomUsuario
    form_class = CustomUsuarioCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return is_admin(self.request.user)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUsuario
    form_class = CustomUsuarioChangeForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return is_admin(self.request.user)

    def get_queryset(self):
        return CustomUsuario.objects.all()


class UserPasswordView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'user_password.html'

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request, pk):
        user = get_object_or_404(CustomUsuario, pk=pk)
        form = CustomSetPasswordForm(user=user)
        return render(request, self.template_name, {'form': form, 'usuario_alvo': user})

    def post(self, request, pk):
        user = get_object_or_404(CustomUsuario, pk=pk)
        form = CustomSetPasswordForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        return render(request, self.template_name, {'form': form, 'usuario_alvo': user})


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CustomUsuario
    template_name = 'user_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return is_admin(self.request.user)


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
    permission_classes = (IsAdminUser, IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserListSerializer
        return UserSerializer


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
    permission_classes = (IsAdminUser, IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserListSerializer
        return UserSerializer