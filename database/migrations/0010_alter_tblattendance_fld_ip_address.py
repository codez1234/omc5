# Generated by Django 4.0.3 on 2022-05-31 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_tblattendance_visit_id_tblattendancelog_visit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblattendance',
            name='fld_ip_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
