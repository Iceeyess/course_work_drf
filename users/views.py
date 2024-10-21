from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.permissions import IsOwnerOrSuperUser
from users.serializiers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework import generics


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class UserDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrSuperUser, )
