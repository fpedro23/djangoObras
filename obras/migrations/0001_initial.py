# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('imagenDependencia', models.FileField(null=True, upload_to=b'', blank=True)),
                ('dependienteDe', models.ForeignKey(blank=True, to='obras.Dependencia', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreEstado', models.CharField(max_length=200)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Impacto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreImpacto', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Inaugurador',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreCargoInaugura', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identificador_unico', models.SlugField(unique=True, null=True)),
                ('registroHacendario', models.CharField(max_length=200)),
                ('registroAuditoria', models.CharField(max_length=200)),
                ('denominacion', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=200)),
                ('fechaInicio', models.DateField()),
                ('fechaTermino', models.DateField()),
                ('inversionTotal', models.DecimalField(max_digits=19, decimal_places=10)),
                ('totalBeneficiarios', models.DecimalField(max_digits=19, decimal_places=10)),
                ('senalizacion', models.BooleanField(default=False)),
                ('susceptibleInauguracion', models.BooleanField(default=False)),
                ('porcentajeAvance', models.DecimalField(max_digits=3, decimal_places=2)),
                ('observaciones', models.CharField(max_length=200)),
                ('fotoAntes', models.FileField(null=True, upload_to=b'', blank=True)),
                ('fotoDurante', models.FileField(null=True, upload_to=b'', blank=True)),
                ('fotoDespues', models.FileField(null=True, upload_to=b'', blank=True)),
                ('fechaModificacion', models.DateField(auto_now=True)),
                ('inaugurada', models.BooleanField(default=False)),
                ('poblacionObjetivo', models.CharField(max_length=200)),
                ('municipio', models.CharField(max_length=200)),
                ('autorizada', models.BooleanField(default=False)),
                ('dependencia', models.ForeignKey(to='obras.Dependencia')),
                ('estado', models.ForeignKey(to='obras.Estado')),
                ('impacto', models.ForeignKey(to='obras.Impacto')),
                ('inaugurador', models.ForeignKey(to='obras.Inaugurador')),
            ],
        ),
        migrations.CreateModel(
            name='TipoClasificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoClasificacion', models.CharField(max_length=200)),
                ('nombreTipoClasificacionCorta', models.CharField(max_length=200)),
                ('subclasificacionDe', models.ForeignKey(blank=True, to='obras.TipoClasificacion', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoInversion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoInversion', models.CharField(max_length=200)),
                ('nombreTipoInversionCorta', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMoneda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoDeMoneda', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TipoObra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombreTipoObra', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rol', models.CharField(default=b'US', max_length=2, choices=[(b'SA', b'Administrador General'), (b'AD', b'Administrador de Dependencia'), (b'US', b'Usuario de Dependencia')])),
                ('dependencia', models.ForeignKey(blank=True, to='obras.Dependencia', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoClasificacion',
            field=models.ManyToManyField(to='obras.TipoClasificacion'),
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoInversion',
            field=models.ManyToManyField(to='obras.TipoInversion'),
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoMoneda',
            field=models.ForeignKey(blank=True, to='obras.TipoMoneda', null=True),
        ),
        migrations.AddField(
            model_name='obra',
            name='tipoObra',
            field=models.ForeignKey(to='obras.TipoObra'),
        ),
    ]
