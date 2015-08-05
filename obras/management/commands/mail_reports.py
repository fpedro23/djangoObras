from django.core.mail import send_mail

from django.core.management.base import BaseCommand
from obras.models import *
from datetime import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        today = datetime.now()

        print '[%s/%s/%s %s:%s:%s] Inicializando envio de correos' % today.day, today.month, today.year, today.hour, today.minute, today.second

        for dependencia in Dependencia.objects.all():
            print '[%s/%s/%s %s:%s:%s] Buscando obras para dependencia %s' % today.day, today.month, today.year, today.hour, today.minute, today.second, dependencia.nombreDependencia
            obras = Obra.objects.filter(Q(dependencia=dependencia) & Q(autorizada=False))

            content = 'Las siguientes obras de la dependencia %s tienen cambios sin autorizar: \n' % dependencia.nombreDependencia
            for obra in obras:
                content += '\t- %s\n' % obra.identificador_unico

            print '[%s/%s/%s %s:%s:%s] Enviando correos' % today.day, today.month, today.year, today.hour, today.minute, today.second
            for contacto in dependencia.get_contactos():
                try:
                    send_mail('Reporte de obras por autorizar',
                          content,
                          'edicomexsa@gmail.com', [contacto.email])
                    print '[%s/%s/%s %s:%s:%s] Correo enviado a %s' % today.day, today.month, today.year, today.hour, today.minute, today.second, contacto.user.email
                except Exception as e:
                    print '[%s/%s/%s %s:%s:%s] Error al enviar correo a %s' % today.day, today.month, today.year, today.hour, today.minute, today.second, contacto.user.email
                    print '[%s/%s/%s %s:%s:%s] %s' % today.day, today.month, today.year, today.hour, today.minute, today.second, e.message
            print 'Finalizando envio de correos'