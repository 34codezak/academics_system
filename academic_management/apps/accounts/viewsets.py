from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, ViewSet

from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from .models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = (IsAuthenticated)
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)
    
    def get_object(self):
        obj = User.objects.get_object_by_username(self.kwargs['pk'])

        self.check_object_permissions(self.request, obj)

        return obj


class RegisterViewSet(ViewSet):
    serializer_class = RegisterSerializer
    permission_class = (AllowAny)
    http_method_names = ['post']

    def create(self, refresh,request , *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response({
            "user": serializer.data,
            "refresh": res("refresh"),
            "token": res["access"]
        },
        status=status.HTTP_201_CREATED
        )

from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_class = (AllowAny)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
