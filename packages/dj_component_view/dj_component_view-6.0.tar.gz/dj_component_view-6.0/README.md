# dj_component_view

This project lets you create reusable Django views from [jinjax](https://jinjax.scaletti.dev/) templates.

## Usage

### templates/components/Greeting.jinja

```jinja
<h1>hello, {{ name }}</h1>
```

### views.py

```python
from dj_component_view import ComponentView
from djecorator import Route

route = Route()

@route("/")
class IndexView(ComponentView):
    template = "components/Index.jinja"


@route("/greet", name="greet")
class GreetView(ComponentView):
    template = "components/Greeting.jinja"

    def context(self, request):
        return {
            "name": request.GET.get("name", "World"),
        }
```

### templates/components/Index.jinja with [htmx](https://htmx.org)

```html
<form hx-get="{{ url('greet') }}" hx-trigger="submit">
  <input type="text" name="name" placeholder="Enter your name" />
  <button type="submit">Greet</button>
</form>
```

### Specifying the Allowed HTTP Methods

You can set the `methods` class variable in your ComponentView subclass to specify the allowed HTTP methods for the view. The default value is `["GET"]`.

- If `methods` is set to `["GET"]`, only GET requests will be allowed.
- If `methods` is set to `["POST"]`, only POST requests will be allowed.
- If `methods` is set to `["GET", "POST"]`, both GET and POST requests will be allowed.

```python
class CustomView(ComponentView):
    component = "CustomComponent"
    methods = ["post"]

    ...

```

If the incoming request's method does not match any of the specified methods, a 405 Method Not Allowed response will be returned.

### Overriding the get and post Methods

If you need more control over the handling of GET and POST requests, you can override the get and post methods in your ComponentView subclass.

```python
@route("/custom")
class CustomView(ComponentView):
    component = "CustomComponent"
    methods = ["get"]

    def get(self, request, *args, **kwargs):
        # Custom implementation of the GET method
        ...
```
