#!/usr/bin/env python
from django.core.management import execute_from_command_line
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stubdjango.settings')
execute_from_command_line(['manage.py', 'shell']) # shell専
