# myapp/management/commands/datacontrol.py
import os
from django.core import serializers
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import DEFAULT_DB_ALIAS, connections, transaction
from django.db.models.deletion import Collector

class Command(BaseCommand):
    help = 'Export, clear, and import database data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--export',
            type=str,
            help='Export data to specified file (JSON format)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear database data (managed models only)'
        )
        parser.add_argument(
            '--clear-all',
            action='store_true',
            help='Clear ALL database data including unmanaged models'
        )
        parser.add_argument(
            '--import',
            type=str,
            dest='import_file',
            help='Import data from specified file'
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Skip confirmation prompts'
        )

    def handle(self, *args, **options):
        # Handle export
        if options['export']:
            self.export_data(options['export'])
        
        # Handle clear
        if options['clear'] or options['clear_all']:
            self.clear_database(
                clear_unmanaged=options['clear_all'],
                noinput=options['noinput']
            )
        
        # Handle import
        if options['import_file']:
            self.import_data(options['import_file'])

    def export_data(self, output_file):
        self.stdout.write(f"Exporting data to {output_file}...")
        try:
            with open(output_file, 'w') as f:
                call_command('dumpdata', format='json', indent=2, stdout=f)
            self.stdout.write(self.style.SUCCESS(f"Data exported successfully to {output_file}"))
        except Exception as e:
            raise CommandError(f"Export failed: {str(e)}")

    def clear_database(self, clear_unmanaged=False, noinput=False):
        if not noinput:
            confirm = input(
                "\nWARNING: This will IRREVERSIBLY DELETE ALL database data.\n"
                "Type 'yes' to continue, or 'no' to cancel: "
            )
            if confirm != 'yes':
                self.stdout.write("Operation cancelled.")
                return

        # Clear managed models
        self.stdout.write("Clearing managed models...")
        call_command('flush', '--noinput')
        
        # Clear unmanaged models if requested
        if clear_unmanaged:
            self.stdout.write("Clearing unmanaged models...")
            unmanaged_models = [
                m for m in apps.get_models() 
                if not m._meta.managed and not m._meta.auto_created
            ]
            
            with transaction.atomic():
                collector = Collector(using=DEFAULT_DB_ALIAS)
                for model in unmanaged_models:
                    collector.add(model.objects.all())
                collector.delete()
                
            self.stdout.write(self.style.SUCCESS("Unmanaged models cleared"))

        self.stdout.write(self.style.SUCCESS("Database cleared successfully"))

    def import_data(self, input_file):
        if not os.path.exists(input_file):
            raise CommandError(f"Input file not found: {input_file}")
        
        self.stdout.write(f"Importing data from {input_file}...")
        try:
            call_command('loaddata', input_file)
            self.stdout.write(self.style.SUCCESS("Data imported successfully"))
        except Exception as e:
            raise CommandError(f"Import failed: {str(e)}")
