from django import forms
from obras.models import Obra, DetalleInversion, DetalleClasificacion, DocumentoFuente
from datetime import datetime
from django.utils.safestring import mark_safe
import os
from django.conf import settings


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """

    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class DetalleClasificacionAddForm(forms.ModelForm):
    class Meta:
        model = DetalleClasificacion
        fields = '__all__'

    def save(self, commit=True):
        instance = super(DetalleClasificacionAddForm, self).save(commit=False)
        print instance.tipoClasificacion
        if instance.tipoClasificacion is None:
            print 'Is null'
            DetalleClasificacion.delete(instance)
            return
        return super(DetalleClasificacionAddForm, self).save(commit)


class DocumentoFuenteForm(forms.ModelForm):
    class Meta:
        model = DocumentoFuente
        fields = "__all__"

    def save(self, commit=True):
        print "OVERAID"
        instance = super(DocumentoFuenteForm, self).save(commit=False)

        if instance.id is not None:  # Revisa si existe ese objeto
            a = DocumentoFuente.objects.filter(id=instance.id).first()

            if a.documento.name != "":  # revisa si tiene una foto asignada

                if instance.documento.name != a.documento.name:  # revisa si cambio la foto asignada
                    route = settings.MEDIA_ROOT + "/" + a.documento.name  # borra la anterior y pon la nueva
                    print route
                    try:
                        os.remove(route)
                    except Exception as e:
                        print e

        return super(DocumentoFuenteForm, self).save(commit)


class DetalleInversionAddForm(forms.ModelForm):
    class Meta:
        model = DetalleInversion
        fields = '__all__'

    def save(self, commit=True):
        instance = super(DetalleInversionAddForm, self).save(commit=False)
        print instance.tipoInversion
        if instance.tipoInversion is None:
            print 'IS NULL'
            DetalleInversion.delete(instance)
            return
        return super(DetalleInversionAddForm, self).save(commit)


class AddObraForm(forms.ModelForm):

    class Meta:
        model = Obra
        fields = '__all__'
        customClearableInput = forms.ClearableFileInput()
        customClearableInput.clear_checkbox_label = 'Borrar'


        widgets = {'tipoMoneda': forms.RadioSelect(renderer=HorizRadioRenderer),
                   'inaugurada': forms.RadioSelect(),
                   'descripcion': forms.Textarea,
                   'observaciones': forms.Textarea,
                   'tipoClasificacion': forms.CheckboxSelectMultiple,
                   'tipoInversion': forms.CheckboxSelectMultiple,
                   'fotoAntes': customClearableInput,
                   'fotoDurante': customClearableInput,
                   'fotoDespues': customClearableInput,
                   }

    def save(self, commit=True):
        instance = super(AddObraForm, self).save(commit=False)
        try:
            instance.dependencia.fecha_ultima_modificacion = datetime.now()
            instance.dependencia.save()
        except Exception as e:
            print e

        if instance.identificador_unico is None:

            lista = Obra.objects.filter(dependencia__id=instance.dependencia.id).values('identificador_unico').order_by('-identificador_unico')

            if lista.count() > 0:
                last_number = lista[0]
                numero = int(last_number.get('identificador_unico').split('_')[2]) + 1
                print numero
                string_id = '%s_%s_%.5d' % ('OB', instance.dependencia.nombreDependencia.upper(), numero)
                string_id.upper()
                instance.identificador_unico = string_id
            else:
                numero = 1
                string_id = '%s_%s_%.5d' % ('OB', instance.dependencia.nombreDependencia.upper(), numero)
                string_id.upper()
                instance.identificador_unico = string_id

        # http://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed
        if instance.id is not None: #Revisa si existe ese objeto
            a = Obra.objects.filter(id=instance.id).first()

            if a.fotoAntes.name != "":  # revisa si tiene una foto asignada

                if instance.fotoAntes.name != a.fotoAntes.name:  # revisa si cambio la foto asignada
                    route = settings.MEDIA_ROOT + "/" + a.fotoAntes.name  # borra la anterior y pon la nueva
                    print route
                    try:
                        os.remove(route)
                    except Exception as e:
                        print e

            if a.fotoDurante.name != "":  # revisa si tiene una foto asignada

                if instance.fotoDurante.name != a.fotoDurante.name:  # revisa si cambio la foto asignada
                    route = settings.MEDIA_ROOT + "/" + a.fotoDurante.name  # borra la anterior y pon la nueva
                    print route
                    try:
                        os.remove(route)
                    except Exception as e:
                        print e

            if a.fotoDespues.name != "":  # revisa si tiene una foto asignada

                if instance.fotoDespues.name != a.fotoDespues.name:  # revisa si cambio la foto asignada
                    route = settings.MEDIA_ROOT + "/" + a.fotoDespues.name  # borra la anterior y pon la nueva
                    print route
                    try:
                        os.remove(route)
                    except Exception as e:
                        print e

        return super(AddObraForm, self).save(commit=commit)