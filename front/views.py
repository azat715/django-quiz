from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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


class Quiz(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Викторина"
        return context


@login_required
def quiz(request, slug):
    return render(request, "quiz.html", {"title": "Викторина", "slug": slug})
