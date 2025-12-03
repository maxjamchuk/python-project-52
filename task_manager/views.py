from django.views.generic import TemplateView
import rollbar


class IndexView(TemplateView):
    template_name = "index.html"
