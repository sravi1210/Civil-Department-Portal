# Generated by Django 2.1.4 on 2019-03-13 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave_portal', '0004_auto_20190313_2218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taslip',
            name='SentTo',
        ),
    ]