from django.core.management.base import BaseCommand, CommandError
from indicators.models import *
from indicators.import_helpers import * 


class Command(BaseCommand):

    args = '<filename>'
    help = 'Imports an indicator from excel file format (xlsx)'

    def handle(self, *args, **options):
        filename = args[0]

        print filename
        try:
            loader = XLSXLoader()
            info, meta, klasses, data = loader.load_xlsx_file(filename)
            update_indicator(info, meta, klasses, data, update=False)


        except Exception, e:  
            import traceback            
            traceback.print_exc()
            raise e

            
        #raise CommandError('Poll "%s" does not exist' % poll_id)
        #self.stdout.write('Successfully closed poll "%s"' % poll_id)
            

            