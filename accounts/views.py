from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import generic

from .forms import RegisterForm


class SignUpView(generic.FormView):
    form_class = RegisterForm
    success_url = reverse_lazy("todo:home")
    template_name = "accounts/register.html"

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
