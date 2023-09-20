from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'lit_common/main.html'
