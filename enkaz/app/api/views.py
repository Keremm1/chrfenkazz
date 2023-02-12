from .serializers import *
from rest_framework import viewsets
from app.models import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .permissions import IsAnonymous
import jwt
import datetime
from rest_framework import permissions


class IsJWTAuthenticatedOrSessionAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        # JWT token var mı kontrol et
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            # JWT token geçerli mi kontrol et
            try:
                jwt.decode(jwt_token, 'secret_key', algorithms=['HS256'])
                return True
            except jwt.PyJWTError:
                return False
        else:
            # JWT token yoksa Django session ile kontrol et
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsNotJWTAuthenticatedOrSessionAuthenticated(permissions.BasePermission):
    def has_permissio(self, request, view):
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            return False
        return not request.user.is_authenticated


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class RegisterViewSet(APIView):
    permission_classes = [IsNotJWTAuthenticatedOrSessionAuthenticated]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, email=" ", password=password)
        user.save()
        return Response("Kayıt başarılı", status=status.HTTP_200_OK)


class LoginViewSet(APIView):
    permission_classes = [IsNotJWTAuthenticatedOrSessionAuthenticated]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if not request.COOKIES.get('allow_cookies'):
                payload = {
                    'username': user.username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
                }
                token = jwt.encode(payload, 'secret_key', algorithm='HS256')
                request.headers['Authorization'] = token
                return Response({'token': token.decode('utf-8')})
            else:
                username = request.data.get('username')
                password = request.data.get('password')
                user = authenticate(username=username, password=password)
                login(request, user)
                return Response("Giriş başarılı", status=status.HTTP_200_OK)
        else:
            return Response("Giriş başarısız", status=status.HTTP_401_UNAUTHORIZED)


class LogoutViewSet(APIView):
    permission_classes = [IsJWTAuthenticatedOrSessionAuthenticated]

    def post(self, request, format=None):
        if request.headers.get('Authorization', None):
            request.headers['Authorization'] = None
        else:
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
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsJWTAuthenticatedOrSessionAuthenticated]
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
        instance = serializer.save(
            user=request.user, ip=request.META.get('REMOTE_ADDR'))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HelpModelViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsJWTAuthenticatedOrSessionAuthenticated]
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
