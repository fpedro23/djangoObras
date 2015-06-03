from django import forms
from django.utils.text import slugify
from obras.models import Obra
import itertools


class AddObraForm(forms.ModelForm):

    class Meta:
        model = Obra
        fields = '__all__'
        widgets = {'tipoMoneda': forms.RadioSelect,
                   'inaugurada': forms.RadioSelect,
        }

    def save(self, commit=True):
        instance = super(AddObraForm, self).save(commit=False)

        if instance.identificador_unico is None:

            for x in itertools.count(1):
                string_id = '%s-%s-%.3d' % ('OB', instance.dependencia.nombreDependencia, x)
                string_id.upper()
                instance.identificador_unico = string_id
                if not Obra.objects.filter(identificador_unico=instance.identificador_unico).exists():
                    break

        print(instance.identificador_unico)
        return super(AddObraForm, self).save(commit=commit)