from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'misc/author.html'


class AboutTechView(TemplateView):
    template_name = 'misc/tech.html'
