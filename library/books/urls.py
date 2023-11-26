from django.urls import path

from .views import BookListCreateView, BookRetrieveUpdateDestroyView, UserLoginView, UserRegisterView, \
    UserLogoutView, UserRegisterDoneView, user_activate, CreateUserView, index

app_name = 'books'

urlpatterns = [
    path('books/<int:pk>', BookRetrieveUpdateDestroyView.as_view(), name='book-rud'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),

    path('accounts/register-user/', CreateUserView.as_view(), name='create-user'),

    path('accounts/activate/<str:sign>/', user_activate, name='activate'),

    path('accounts/login/', UserLoginView.as_view(), name='login'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),

    path('accounts/register/done/', UserRegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', UserRegisterView.as_view(), name='register'),
    path('accounts/register/', UserRegisterView.as_view(), name='password_reset'),
    
    
    path('', index, name='index'),
]
