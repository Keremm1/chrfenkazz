from .serializers import *
from rest_framework import viewsets
from app.models import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsAnonymous, IsAdminUserorIsOwner, IsAdminUserorIsAnonymous


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAdminUser]

class RegisterViewSet(APIView):
    permission_classes = [IsAdminUserorIsAnonymous]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, email=None, password=password)
        user.save()
        return Response("Kayıt başarılı", status=status.HTTP_200_OK)


class LoginViewSet(APIView):
    permission_classes = [IsAnonymous]
    def get(self, request, format=None):
        return Response(request.session, status=status.HTTP_200_OK)
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return Response("Giriş başarılı", status=status.HTTP_200_OK)
        else:
            return Response("Giriş başarısız", status=status.HTTP_401_UNAUTHORIZED)


class LogoutViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response("Çıkış başarılı", status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    lookup_field = 'id'


class CanModelViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUserorIsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    serializer_class = CanModelSerializer
    queryset = CanModel.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user
        request.data['ip'] = request.META.get('REMOTE_ADDR')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, ip=request.META.get('REMOTE_ADDR'))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



class HelpModelViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUserorIsOwner]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    serializer_class = HelpModelSerializer
    queryset = HelpModel.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        category = request.data.get('category')
        category = CategoryModel.objects.get(name=category)

        request.data['category'] = category
        request.data['user'] = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

