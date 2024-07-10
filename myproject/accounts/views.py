# accounts/views.py
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm


class DefaultLoginView(LoginView):
    next_page = "books:index"


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:login")
    template_name = "registration/signup.html"
