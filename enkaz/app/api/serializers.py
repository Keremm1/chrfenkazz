from rest_framework import serializers
from app.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id', 'name', 'help_count', 'can_count')

class CanModelSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=CategoryModel.objects.all())
    class Meta:
        model = CanModel
        fields = ('id', 'user','description', 'category','city', 'town', 'street', 'neighbourhood', 'phone',  'ip','username')
        read_only_fields = ('id','user','ip')


class HelpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpModel
        fields = ('id','user', 'category', 'description', 'city', 'town', 'street', 'neighbourhood', 'phone','username')
        read_only_fields = ('id','user')

