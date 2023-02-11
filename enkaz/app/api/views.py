from .serializers import *
from rest_framework import viewsets
from app.models import *
from rest_framework.response import Response
from rest_framework import status

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
