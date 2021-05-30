from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class QuizzesList(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Викторина"
        return context
