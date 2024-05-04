from importlib import import_module

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views import View


class ComponentView(View):
    component = None
    methods = ["GET"]

    def get_catalog(self):
        for template_engine in settings.TEMPLATES:
            if template_engine["BACKEND"] == "django.template.backends.jinja2.Jinja2":
                env_string = template_engine["OPTIONS"]["environment"]
                module_path, function_name = env_string.rsplit(".", 1)
                module = import_module(module_path)
                environment_function = getattr(module, function_name)
                return environment_function().globals["catalog"]
        raise ValueError("Jinja2 template engine not found in settings.")

    def render_to_response(self, context):
        catalog = self.get_catalog()
        catalog.jinja_env.globals.update(context)
        if not self.component:
            raise ValueError("ComponentView subclasses must define a component.")
        return HttpResponse(str(catalog.render(self.component, **context)))

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in (method.lower() for method in self.methods):
            return HttpResponseNotAllowed(self.methods)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.context(request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.context(request)
        return self.render_to_response(context)

    def context(self, request):
        return {}
