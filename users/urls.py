from users.apps import UsersConfig
from users.views import MyTokenObtainPairView, UserRegister, UserDelete
from django.urls import path


app_name = UsersConfig.name


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token'),
    path('register/', UserRegister.as_view(), name='user-register'),
    path('delete/<int:pk>/', UserDelete.as_view(), name='user-delete'),
]



