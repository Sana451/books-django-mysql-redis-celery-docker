from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import BadSignature
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, TemplateView
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import Book, AdvUser
from .serializers import BookSerializer, UserSerializer
from .tasks import signer


def index(request):
    return render(request, 'main/index.html')


class BookListCreateView(ListCreateAPIView):
    """Реализует вывод списка книг (GET запрос на url http://0.0.0.0:8000/api/books/),
    а также создание новой книги (POST запрос на тот же url, с телом запроса вида:
    {"title": "Книга 1",
    "year_of_publication": "2023-11-25T15:14",
    "isbn": "1232345678987",
    "author": 1})
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)


class BookRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Реализует вывод информации о конкретной книге (GET запрос на url http://0.0.0.0:8000/api/books/1),
    изменение данных книги (PUT запрос на тот же url, с телом запроса вида:
    {"title": "Книга 1",
    "year_of_publication": "2023-11-25T15:14",
    "isbn": "1232345678987",
    "author": 1}),
    а также удаление книги (DELETE запрос на тот же url)
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly,)


class UserLoginView(LoginView):
    template_name = 'main/login.html'


class UserLogoutView(LogoutView):
    pass  # т.к. в settings.py LOGOUT_REDIRECT_URL = 'index'
    # альтернатива:
    # template_name = 'index.html'


class UserRegisterView(CreateView):
    model = AdvUser
    template_name = 'main/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('books:register_done')


class UserRegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/activation_failed.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/activation_done_earlier.html'
    else:
        template = 'main/activation_done.html'
        user.is_activated = True
        user.save()
    return render(request, template)


class CreateUserView(CreateAPIView):
    """Класс реализует создание нового пользователя (POST запрос на url http://0.0.0.0:8000/api/accounts/register-user/,
    с телом
    {"username": "New User",
    "email": "new_user@gmail.com",
    "password": "Qwertyu123ererre"}).
    В сериализаторе UserSerializer переопределён метод create, вызывающий асинхронную задачу
    send_activation_notification, которая использует Celery (Redis в качестве брокера) для отправки email сообщения
    со ссылкой на страницу подтверждения регистрации нового пользователя.
    """
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
