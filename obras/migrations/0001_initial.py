# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreDependencia', models.CharField(max_length=200)),
                ('imagenDependencia', models.FileField(null=True, upload_to=b'./', blank=True)),
                ('obraoprograma', models.CharField(max_length=1, null=True, blank=True)),
                ('dependienteDe', models.ForeignKey(blank=True, to='obras.Dependencia', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentoFuente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=50, null=True, blank=True)),
                ('documento', models.FileField(null=True, upload_to=b'/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreEstado', models.CharField(max_length=200)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Impacto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreImpacto', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inaugurador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreCargoInaugura', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InstanciaEjecutora',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identificador_unico', models.SlugField(unique=True, null=True)),
                ('registroHacendario', models.CharField(max_length=200, null=True, blank=True)),
                ('montoRegistroHacendario', models.FloatField(null=True, verbose_name=b'Recursos Federales Autorizados', blank=True)),
                ('denominacion', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('fechaInicio', models.DateField()),
                ('fechaTermino', models.DateField(verbose_name=b'Fecha de Termino')),
                ('inversionTotal', models.DecimalField(max_digits=19, decimal_places=10)),
                ('totalBeneficiarios', models.DecimalField(max_digits=19, decimal_places=10)),
                ('senalizacion', models.BooleanField(default=False)),
                ('susceptibleInauguracion', models.BooleanField(default=False)),
                ('porcentajeAvance', models.DecimalField(max_digits=3, decimal_places=2)),
                ('observaciones', models.CharField(max_length=200)),
                ('fotoAntes', models.FileField(null=True, upload_to=b'', blank=True)),
                ('fotoDurante', models.FileField(null=True, upload_to=b'', blank=True)),
                ('fotoDespues', models.FileField(null=True, upload_to=b'', blank=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True, auto_now_add=True)),
                ('inaugurada', models.NullBooleanField(choices=[(True, b'Si'), (False, b'No'), (None, b'Sin inauguracion')])),
                ('poblacionObjetivo', models.CharField(max_length=200)),
                ('municipio', models.CharField(max_length=200)),
                ('autorizada', models.BooleanField(default=False)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('dependencia', models.ForeignKey(related_name='obra_dependencia', to='obras.Dependencia')),
                ('estado', models.ForeignKey(to='obras.Estado')),
                ('impacto', models.ForeignKey(to='obras.Impacto')),
                ('inaugurador', models.ForeignKey(to='obras.Inaugurador')),
                ('instanciaEjecutora', models.ForeignKey(blank=True, to='obras.InstanciaEjecutora', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoClasificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoClasificacion', models.CharField(max_length=200)),
                ('nombreTipoClasificacionCorta', models.CharField(max_length=200)),
                ('subclasificacionDe', models.ForeignKey(blank=True, to='obras.TipoClasificacion', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoInversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoInversion', models.CharField(max_length=200)),
                ('nombreTipoInversionCorta', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoMoneda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoDeMoneda', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoObra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoObra', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.SlugField(unique=True, null=True)),
                ('tipoObra', models.CharField(max_length=50)),
                ('lat', models.CharField(max_length=50)),
                ('lng', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('dependencia', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rol', models.CharField(default=b'US', max_length=2, choices=[(b'SA', b'Administrador General'), (b'AD', b'Administrador de Dependencia'), (b'US', b'Usuario de Dependencia')])),
                ('dependencia', models.ManyToManyField(to='obras.Dependencia', null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='obra',
            name='subclasificacion',
            field=models.ManyToManyField(related_name='obra_subclasificaciones', to='obras.TipoClasificacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='subdependencia',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dependienteDe', to='obras.Dependencia', chained_field=b'dependencia'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoClasificacion',
            field=models.ManyToManyField(related_name='obra_clasificaciones', to='obras.TipoClasificacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoInversion',
            field=models.ManyToManyField(to='obras.TipoInversion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoMoneda',
            field=models.ForeignKey(to='obras.TipoMoneda'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoObra',
            field=models.ForeignKey(to='obras.TipoObra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentofuente',
            name='obra',
            field=models.ForeignKey(blank=True, to='obras.Obra', null=True),
            preserve_default=True,
        ),
    ]
