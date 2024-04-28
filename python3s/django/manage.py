#!/usr/bin/env python
from django.core.management import execute_from_command_line
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stubdjango.settings')
execute_from_command_line(sys.argv[1:] + ( sys.argv[1:] or ['shell',]) ) # shell専
