# Generated by Django 4.0.3 on 2022-05-28 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0005_tblattendancelog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tblattendancelog',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='tblattendancelog',
            name='claim_id',
        ),
        migrations.RemoveField(
            model_name='tblattendancelog',
            name='visit_id',
        ),
    ]
