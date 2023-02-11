from django.contrib.auth import authenticate, login ,logout
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse

class RegisterView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password ,email="default@gmail.com")
        user.save()
        return HttpResponse("Kayıt Başarılı")
class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Giriş Yapıldı")
        return HttpResponse("Kullanıcı adı veya şifre hatalı")
class LogoutView(View,LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return HttpResponse("Çıkış yapıldı")
