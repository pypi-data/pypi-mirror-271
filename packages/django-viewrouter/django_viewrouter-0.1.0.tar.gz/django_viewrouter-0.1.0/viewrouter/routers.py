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

from django.urls import include, path

class Router(object):
    action_allowed = ['index', 'create', 'retrieve', 'update', 'delete']
    action_has_pk = ['retrieve', 'update', 'delete']
    
    def __init__(self, view, urls=None):
        self.view = view
        self.view_name = view.__name__.lower()
        self.urlpatterns = urls

    def build_urlpatterns(self, pattern, action, urlname, http_methods):
        kwargs = {
            'route_action': action,
        }
        if len(http_methods) > 0:
            kwargs['http_method_names'] = http_methods
        urlpatterns = [
                path(pattern, self.view.as_view(**kwargs), name=urlname)
            ]
        return urlpatterns
    
    def build_default_pattern(self, action):
        if action in self.action_has_pk:
            pattern = f'{action}/<int:pk>/'
        else:
            pattern = f'{action}/'
        return pattern
        
    @property
    def urls(self):
        urlpatterns = []
        overidden_actions = []
        for _url in self.view.urls:
            pattern, action, urlname, http_methods = _url
            overidden_actions.append(action)
            urlpatterns += self.build_urlpatterns(
                    pattern,
                    action,
                    urlname, 
                    http_methods
                )

        for action in dir(self.view):
            action_callable = getattr(self.view, action, None)
            if action not in self.action_allowed:
                if not hasattr(action_callable, '_route'):
                    continue
            if action in overidden_actions:
                continue

            _urlname, _http_methods = None, []
            if (action_callable is not None and
                    hasattr(action_callable, '_route')):
                pattern, _urlname, _http_methods = action_callable._route
            else:
                pattern = self.build_default_pattern(action)

            # pattern still None, a case when user using @route decorator
            # but does not specify pattern
            if pattern is None:
                pattern = self.build_default_pattern(action)

            as_view_kwargs = {
                'route_action': action,
            }
            urlpatterns += self.build_urlpatterns(
                            pattern,
                            action,
                            _urlname or action,
                            _http_methods
                        )

            # allow index to be accessed as /
            if action == 'index':
                urlpatterns += self.build_urlpatterns(
                            "",
                            action,
                            _urlname or action,
                            _http_methods
                        )
        return (urlpatterns, self.view_name)

def route(pattern=None, name=None, http_methods=None):
    def decorator(fn):
        fn._route = (pattern, name or fn.__name__, http_methods or [])
        return fn
    return decorator
