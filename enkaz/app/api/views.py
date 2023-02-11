from .serializers import *
from rest_framework import viewsets
from app.models import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

class RegisterViewSet(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response("Kayıt başarılı", status=status.HTTP_200_OK)

class LoginViewSet(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response("Giriş başarılı", status=status.HTTP_200_OK)
        else:
            return Response("Giriş başarısız", status=status.HTTP_401_UNAUTHORIZED)

class LogoutViewSet(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, format=None):
        logout(request)
        return Response("Çıkış başarılı", status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()
    lookup_field = 'id'

class CanModelViewSet(viewsets.ModelViewSet):
    serializer_class = CanModelSerializer
    queryset = CanModel.objects.all()
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user
        request.data['ip'] = request.META.get('REMOTE_ADDR')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=request.user, ip=request.META.get('REMOTE_ADDR'))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HelpModelViewSet(viewsets.ModelViewSet):
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
