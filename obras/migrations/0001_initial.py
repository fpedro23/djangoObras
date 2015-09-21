# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields
from django.conf import settings
import obras.models


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
                ('imagenDependencia', models.FileField(null=True, upload_to=obras.models.content_file_dependencia, blank=True)),
                ('obraoprograma', models.CharField(default=b'O', max_length=1, null=True, blank=True)),
                ('fecha_ultima_modificacion', models.DateTimeField(null=True, blank=True)),
                ('orden_secretaria', models.FloatField(null=True, blank=True)),
                ('dependienteDe', models.ForeignKey(blank=True, to='obras.Dependencia', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleClasificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DetalleInversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monto', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentoFuente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=50)),
                ('documento', models.FileField(upload_to=obras.models.content_file_documento_fuente)),
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
                'verbose_name': 'Tipo de Impacto',
                'verbose_name_plural': 'Tipos de Impacto',
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
                'verbose_name': 'Inaugurador',
                'verbose_name_plural': 'Inauguradores',
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
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreMunicipio', models.CharField(max_length=200)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('estado', models.ForeignKey(to='obras.Estado')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identificador_unico', models.SlugField(unique=True, null=True, verbose_name=b'Identificador \xc3\x9anico')),
                ('registroHacendario', models.CharField(max_length=200, null=True, blank=True)),
                ('montoRegistroHacendario', models.FloatField(null=True, verbose_name=b'Recursos Federales Autorizados', blank=True)),
                ('denominacion', models.CharField(max_length=200, verbose_name=b'Denominaci\xc3\xb3n')),
                ('descripcion', models.CharField(max_length=200)),
                ('fechaInicio', models.DateField(verbose_name=b'Fecha de Inicio')),
                ('fechaTermino', models.DateField(verbose_name=b'Fecha de T\xc3\xa9rmino')),
                ('inversionTotal', models.FloatField()),
                ('totalBeneficiarios', models.IntegerField()),
                ('senalizacion', models.BooleanField(default=False, verbose_name=b'Se\xc3\xb1alizaci\xc3\xb3n')),
                ('susceptibleInauguracion', models.BooleanField(default=False)),
                ('porcentajeAvance', models.DecimalField(max_digits=5, decimal_places=2)),
                ('observaciones', models.CharField(max_length=200, null=True, blank=True)),
                ('fotoAntes', models.FileField(null=True, upload_to=obras.models.content_file_antes, blank=True)),
                ('fotoDurante', models.FileField(null=True, upload_to=obras.models.content_file_durante, blank=True)),
                ('fotoDespues', models.FileField(null=True, upload_to=obras.models.content_file_despues, blank=True)),
                ('fechaModificacion', models.DateTimeField(auto_now=True, verbose_name=b'Fecha de Modificaci\xc3\xb3n', auto_now_add=True)),
                ('inaugurada', models.BooleanField(default=False, choices=[(True, b'S\xc3\xad'), (False, b'No')])),
                ('poblacionObjetivo', models.CharField(max_length=200)),
                ('autorizada', models.BooleanField(default=False)),
                ('latitud', models.FloatField(null=True, blank=True)),
                ('longitud', models.FloatField(null=True, blank=True)),
                ('id_Dependencia', models.CharField(max_length=200, null=True, verbose_name=b'Identificador Interno', blank=True)),
                ('dependencia', models.ForeignKey(related_name='obra_dependencia', to='obras.Dependencia')),
                ('estado', models.ForeignKey(to='obras.Estado')),
                ('impacto', models.ForeignKey(blank=True, to='obras.Impacto', null=True)),
                ('inaugurador', models.ForeignKey(blank=True, to='obras.Inaugurador', null=True)),
                ('instanciaEjecutora', models.ForeignKey(blank=True, to='obras.InstanciaEjecutora', null=True)),
                ('municipio', models.ForeignKey(to='obras.Municipio')),
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
                'verbose_name': 'Tipo de Clasificaci\xf3n',
                'verbose_name_plural': 'Tipos de Clasificaci\xf3n',
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
                'verbose_name': 'Tipo de Inversi\xf3n',
                'verbose_name_plural': 'Tipos de Inversi\xf3n',
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
                ('subdependencia', models.ManyToManyField(related_name='Subdependencias', null=True, to='obras.Dependencia', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='obra',
            name='subclasificacion',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'subclasificacionDe', related_name='obra_subclasificaciones', chained_field=b'tipoClasificacion', blank=True, to='obras.TipoClasificacion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='subdependencia',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dependienteDe', chained_field=b'dependencia', blank=True, to='obras.Dependencia', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoClasificacion',
            field=models.ManyToManyField(db_constraint=obras.models.TipoClasificacion, null=True, through='obras.DetalleClasificacion', to='obras.Obra', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoInversion',
            field=models.ManyToManyField(to='obras.TipoInversion', null=True, through='obras.DetalleInversion', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoMoneda',
            field=models.ForeignKey(default=1, to='obras.TipoMoneda'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoObra',
            field=models.ForeignKey(verbose_name=b'Tipo de Obra', to='obras.TipoObra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentofuente',
            name='obra',
            field=models.ForeignKey(to='obras.Obra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalleinversion',
            name='obra',
            field=models.ForeignKey(to='obras.Obra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalleinversion',
            name='tipoInversion',
            field=models.ForeignKey(to='obras.TipoInversion'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='detalleinversion',
            unique_together=set([('obra', 'tipoInversion')]),
        ),
        migrations.AddField(
            model_name='detalleclasificacion',
            name='obra',
            field=models.ForeignKey(to='obras.Obra'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalleclasificacion',
            name='subclasificacion',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'subclasificacionDe', related_name='obra_subclasificacion', chained_field=b'tipoClasificacion', blank=True, to='obras.TipoClasificacion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalleclasificacion',
            name='tipoClasificacion',
            field=models.ForeignKey(related_name='obra_clasificacion', blank=True, to='obras.TipoClasificacion', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='detalleclasificacion',
            unique_together=set([('obra', 'tipoClasificacion')]),
        ),
    ]
