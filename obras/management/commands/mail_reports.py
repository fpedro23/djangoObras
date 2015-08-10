from django.core.mail import send_mail

from django.core.management.base import BaseCommand
from obras.models import *
from datetime import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.now()

        print '[{0}/{1}/{2} {3}:{4}:{5}] Inicializando envio de correos'.format(today.day, today.month, today.year, today.hour, today.minute, today.second)

        for dependencia in Dependencia.objects.all():
            print '[{0}/{1}/{2} {3}:{4}:{5}] Buscando obras para dependencia {6}'.format(today.day, today.month, today.year, today.hour, today.minute, today.second, dependencia.nombreDependencia)
            obras = Obra.objects.filter(Q(dependencia=dependencia) & Q(autorizada=False))

            content = 'Las siguientes obras de la dependencia {0} tienen cambios sin autorizar: \n'.format(dependencia.nombreDependencia)
            for obra in obras:
                content += '\t- {0}\n'.format(obra.identificador_unico)

            print '[{0}/{1}/{2} {3}:{4}:{5}] Enviando correos'.format(today.day, today.month, today.year, today.hour, today.minute, today.second)
            for contacto in dependencia.get_contactos():
                try:
                    send_mail('Reporte de obras por autorizar',
                          content,
                          'edicomexsa@gmail.com', [contacto.email])
                    print '[{0}/{1}/{2} {3}:{4}:{5}] Correo enviado a {6}'.format(today.day, today.month, today.year, today.hour, today.minute, today.second, contacto.user.email)
                except Exception as e:
                    print '[{0}/{1}/{2} {3}:{4}:{5}] Error al enviar correo a {6}'.format(today.day, today.month, today.year, today.hour, today.minute, today.second, contacto.user.email)
                    print '[{0}/{1}/{2} {3}:{4}:{5}] {6}'.format(today.day, today.month, today.year, today.hour, today.minute, today.second, e.message)
            print 'Finalizando envio de correos'