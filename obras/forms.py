from django import forms
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

        if instance.identificador_unico is None:

            for x in itertools.count(1):
                string_id = '%s-%s-%.3d' % ('OB', instance.dependencia.nombreDependencia, x)
                string_id.upper()
                instance.identificador_unico = string_id
                if not Obra.objects.filter(identificador_unico=instance.identificador_unico).exists():
                    break

        print(instance.identificador_unico)
        return super(AddObraForm, self).save(commit=commit)