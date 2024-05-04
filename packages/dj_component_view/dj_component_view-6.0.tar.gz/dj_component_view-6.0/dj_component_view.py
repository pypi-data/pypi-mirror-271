from importlib import import_module
from typing import Union

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views import View
from django.shortcuts import render


class ComponentView(View):
    template = None
    methods = ["GET", "POST"]

    def get_catalog(self):
        for template_engine in settings.TEMPLATES:
            if template_engine["BACKEND"] == "django.template.backends.jinja2.Jinja2":
                env_string = template_engine["OPTIONS"]["environment"]
                module_path, function_name = env_string.rsplit(".", 1)
                module = import_module(module_path)
                environment_function = getattr(module, function_name)
                return environment_function().globals["catalog"]
        raise ValueError("Jinja2 template engine not found in settings.")


    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in (method.lower() for method in self.methods):
            return HttpResponseNotAllowed(self.methods)
        return super().dispatch(request, *args, **kwargs)
    
    def _base_get_post(self, request, *args, **kwargs):
        ctx = self.render(request)
        template = self.template

        if isinstance(ctx, HttpResponse):
            return ctx
        
        return render(
            request=request,
            template_name=template,
            context=ctx,
        )

    def get(self, request, *args, **kwargs):
        return self._base_get_post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self._base_get_post(request, *args, **kwargs)

    def render(self, request) -> Union[dict, HttpResponse, None]:
        return {}
