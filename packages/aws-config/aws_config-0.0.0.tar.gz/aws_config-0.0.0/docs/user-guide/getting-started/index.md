# Quick Start


Install:

```shell
pip install django-umami
```

Use as a decorator for your django view:
```python
import djade.decorators

@djade.decorators.track("my custom event!")
def myview(request):
    ...
```

Or use standalone:
```python
import djade.core

def myview(request):
    djade.core.umami.track("someone went to django view!")
    ...
```


## Content

- [Installation](installation.md)
- [Settings](settings.md)
- [Usage](usage/core.md)