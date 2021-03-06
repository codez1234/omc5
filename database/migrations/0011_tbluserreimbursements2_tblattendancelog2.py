# Generated by Django 4.0.3 on 2022-06-01 14:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0010_alter_tblattendance_fld_ip_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='TblUserReimbursements2',
            fields=[
                ('id', models.AutoField(db_column='fld_ai_id', primary_key=True, serialize=False)),
                ('claim_id', models.CharField(blank=True, db_column='fld_claim_id', max_length=100, null=True)),
                ('visit_id', models.CharField(blank=True, db_column='fld_visit_id', max_length=50, null=True)),
                ('distance', models.IntegerField(blank=True, db_column='fld_distance', null=True)),
                ('amount', models.IntegerField(blank=True, db_column='fld_amount', null=True)),
                ('status', models.CharField(blank=True, choices=[('approved', 'approved'), ('pending', 'pending'), ('requested', 'requested'), ('closed', 'closed')], db_column='fld_status', default='pending', max_length=20, null=True)),
                ('is_active', models.BooleanField(db_column='fld_is_active', default=True)),
                ('is_delete', models.BooleanField(db_column='fld_is_delete', default=False)),
                ('date', models.DateField(blank=True, db_column='fld_date', null=True)),
                ('created_datetime', models.DateTimeField(blank=True, db_column='fld_created_datetime', null=True)),
                ('user_id', models.ForeignKey(blank=True, db_column='fld_user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_user_reimbursements_update',
            },
        ),
        migrations.CreateModel(
            name='TblAttendanceLog2',
            fields=[
                ('id', models.AutoField(db_column='fld_ai_id', primary_key=True, serialize=False)),
                ('visit_id', models.CharField(blank=True, db_column='fld_visit_id', max_length=50, null=True)),
                ('start_latitude', models.FloatField(blank=True, db_column='fld_start_latitude', null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('start_longitude', models.FloatField(blank=True, db_column='fld_start_longitude', null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('end_latitude', models.FloatField(blank=True, db_column='fld_end_latitude', null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('end_longitude', models.FloatField(blank=True, db_column='fld_end_longitude', null=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)])),
                ('start_time', models.TimeField(blank=True, db_column='fld_start_time', null=True)),
                ('end_time', models.TimeField(blank=True, db_column='fld_end_time', null=True)),
                ('date', models.DateField(blank=True, db_column='fld_date', null=True)),
                ('is_active', models.BooleanField(db_column='fld_is_active', default=True)),
                ('is_delete', models.BooleanField(db_column='fld_is_delete', default=False)),
                ('created_datetime', models.DateTimeField(blank=True, db_column='fld_created_datetime', null=True)),
                ('site_id', models.ForeignKey(blank=True, db_column='fld_site_omc_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.tblsites')),
                ('user_id', models.ForeignKey(blank=True, db_column='fld_user_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'tbl_attendance_log_update',
            },
        ),
    ]
