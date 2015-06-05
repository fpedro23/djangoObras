__author__ = 'mng687'
from django.core.management.base import BaseCommand, CommandError
from obras.models import *
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE


class Command(BaseCommand):
    def handle(self, *args, **options):
        print 'Success!'