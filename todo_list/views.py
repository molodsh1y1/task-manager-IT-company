from django.shortcuts import render
from django.views import generic


class HomePageView(generic.TemplateView):
    template_name = "todo_list/index.html"
