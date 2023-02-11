from django.urls import path, include

from .views import *

viewss = {HelpModel: HelpModelViewSet, CategoryModel: CategoryViewSet, CanModel: CanModelViewSet,User: UserViewSet}

from rest_framework import routers

router = routers.DefaultRouter()
for model, view in viewss.items():
    router.register(model.__name__, view)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view()),
    path('logout/', LogoutViewSet.as_view()),
]

