import sys
import inspect

from django.contrib import admin
# flake8: noqa
from .models import *

# get a list of all classes in models.py
list_of_imported_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for imported_class, _ in list_of_imported_classes:
    # register all classes from models.py in admin panel
    admin.site.register(getattr(sys.modules[__name__], imported_class))
