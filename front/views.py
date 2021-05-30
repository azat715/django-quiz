from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class QuizzesList(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Викторина"
        return context
