# Generated by Django 4.0.3 on 2022-06-02 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0012_alter_tbluserreimbursements_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbluserreimbursements',
            name='distance',
            field=models.FloatField(blank=True, db_column='fld_distance', null=True),
        ),
    ]