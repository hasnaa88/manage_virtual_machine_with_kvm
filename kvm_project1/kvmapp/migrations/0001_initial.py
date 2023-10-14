# Generated by Django 3.2.19 on 2023-07-07 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('xml', models.TextField()),
                ('state', models.IntegerField(choices=[(0, 'Shutoff'), (1, 'Running'), (2, 'Paused')])),
                ('memory', models.IntegerField()),
                ('vcpu', models.IntegerField()),
            ],
        ),
    ]