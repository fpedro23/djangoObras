from django import forms
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from obras.models import Obra, Dependencia
from obras.models import Obra, DetalleInversion
import itertools
from datetime import datetime


class DetalleInversionAddForm(forms.ModelForm):
    class Meta:
        model = DetalleInversion


class AddObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = '__all__'
        widgets = {'tipoMoneda': forms.RadioSelect,
                   'inaugurada': forms.RadioSelect,
                   'descripcion': forms.Textarea,
                   'observaciones': forms.Textarea,
                   'tipoClasificacion': forms.CheckboxSelectMultiple,
                   'tipoInversion': forms.CheckboxSelectMultiple
        }

    def save(self, commit=True):
        instance = super(AddObraForm, self).save(commit=False)
        instance.dependencia.fecha_ultima_modificacion = datetime.now()
        print instance.dependencia.fecha_ultima_modificacion
        instance.dependencia.save()

        if instance.id and not instance.autorizada:
            obra = Obra.objects.get(id=instance.id)
            usuario = LogEntry.objects.filter(
                object_id=obra.id,
                action_flag=ADDITION,
                content_type__id__exact=ContentType.objects.get_for_model(Obra).id
            ).order_by('action_time').last().user
            send_mail('Cambios obra %s no autorizados' % obra.identificador_unico,
                      'Los cambios a a la obra %s no fueron autorizados' % obra.identificador_unico,
                      'edicomexsa@gmail.com', [usuario.email])

        if instance.identificador_unico is None:

            for x in itertools.count(1):
                string_id = '%s-%s-%.3d' % ('OB', instance.dependencia.nombreDependencia, x)
                string_id.upper()
                instance.identificador_unico = string_id
                if not Obra.objects.filter(identificador_unico=instance.identificador_unico).exists():
                    break

        print(instance.identificador_unico)
        return super(AddObraForm, self).save(commit=commit)