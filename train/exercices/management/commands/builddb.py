
from django.core.management.base import BaseCommand, CommandError
from train.models import Exercice
from django.conf import settings

class Command(BaseCommand):
    help = 'Generate exercice database'

    def handle(self, *args, **options):
        names = set (map (
            lambda x: x['name'],
            settings.EXERCICES_CONF
        ))
        
        already_builts = Exercice.objects.all()

        for already_built in already_builts:
            if already_built.name in names:
                names.remove(already_built.name)
            else:
                already_built.delete()
        
        for exercice in settings.EXERCICES_CONF:
            if exercice['name'] in names:
                Exercice.objects.create(**exercice)
            else:
                Exercice.objects.filter(name=exercice['name']).update(**exercice)
