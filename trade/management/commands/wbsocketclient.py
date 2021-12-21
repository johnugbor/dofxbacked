from django.core.management.base import BaseCommand
from trade.wsconfig import *

class Command(BaseCommand):

	def handle(self, *args,**options):

		ws_main()