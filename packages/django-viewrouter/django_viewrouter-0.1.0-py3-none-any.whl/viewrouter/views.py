"""
Copyright (c) 2014 Mohd. Kamal Bin Mustafa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.base import View
from django.shortcuts import render

class ActionView(View):
    route_action = 'index'
    urls = []
    template_prefix = None
    model = None

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, self.route_action, self.not_found)
        else:
            handler = self.http_method_not_allowed

        response = handler(request, *args, **kwargs)
        if getattr(response, "is_rendered", None):
            # assume a TemplateResponse
            if not response.template_name:
                response.template_name = self.get_template()
        return response

    def not_found(self, *args, **kwargs):
        return HttpResponseNotFound()

    def get_template(self):
        app_name = self.request.resolver_match.app_name
        class_name = self.__class__.__name__.lower()
        template_name = f"{class_name}_{self.route_action}.html"
        prefix = None
        templates = []

        if self.model:
            prefix = self.model._meta.app_label + "/"
        if self.template_prefix:
            prefix = self.template_prefix

        if prefix:
            templates.append(f"{prefix}{template_name}")
            templates.append(f"{prefix}actionview_{self.route_action}.html")
        templates.append(template_name)
        templates.append(f"viewrouter/actionview_{self.route_action}.html")
        return templates

    def get_object(self, *args, **kwargs):
        if not self.model:
            raise Exception("model not defined")

        return self.model.objects.get(*args, **kwargs)

    def index(self, *args, **kwargs):
        return render(self.request, self.get_template())

    @classmethod
    def get_urls(cls):
        from .routers import Router
        return Router(cls).urls
