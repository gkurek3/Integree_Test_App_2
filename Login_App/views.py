from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginView(View):
    """
    Basic login view with a form to be filled by a user. Logged user is informed of a successful
    logging and can log out.
    Logged in user is stored in a cookie session.
    If logging is unsuccessful, user is informed and can log in again.
    """

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'login_correct.html')
        else:
            return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return render(request, 'login_incorrect.html', {"username": username, "message": "Logowanie nieudane"})
        return render(request, 'login_correct.html', {'username': username})


class LogoutView(View):
    """
    The view logs out a user. It Works with LoginView.
    """
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('login'))


class RestLoginView(APIView):
    """
    Login view using Rest to log a user in. Logged user is informed of a successful
    logging and can log out.
    Logged in user is stored in a cookie session.
    If logging is unsuccessful, user is informed and can log in again.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'login_correct.html'

    def get(self, request):
        if request.user.is_authenticated:
            return Response(template_name='login_correct.html')
        else:
            return Response(template_name='login.html')

    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(template_name="rest_login_correct.html")
            else:
                return Response({"username": username, "message": "Logowanie nieudane"},
                                template_name="login_incorrect.html")
        else:
            return Response({"username": username, "message": "Logowanie nieudane"},
                            template_name="login_incorrect.html")


class RestLogoutView(View):
    """
    The view logs out a user. It works with RestLoginView.
    """
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('rest-login'))
