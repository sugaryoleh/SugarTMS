# Generated by Django 4.0.4 on 2022-05-24 22:11

import app.models.files
import app.models.units
import app.models.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=56)),
                ('city', models.CharField(max_length=35)),
                ('zip', models.CharField(max_length=10, validators=[app.models.validators.validate_zip_code])),
                ('street', models.CharField(max_length=35)),
                ('building', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LogisticsCompany',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('MC', models.CharField(max_length=6, unique=True, validators=[app.models.validators.validate_MC_number])),
                ('DOT', models.CharField(max_length=7, unique=True, validators=[app.models.validators.validate_DOT_number])),
                ('rate', models.CharField(max_length=1, validators=[app.models.validators.validate_logistics_company_rate])),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.address')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
                ('department', models.CharField(choices=[('DRM', 'Driver relationship management'), ('SAFETY', 'Safety'), ('OPERATIONS', 'Operations'), ('SHOP', 'Shop'), ('ACCOUNTING', 'Accounting')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            bases=(models.Model, app.models.units.Unit),
        ),
        migrations.CreateModel(
            name='UnitGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UnitMake',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnitModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BrokerCompany',
            fields=[
                ('logisticscompany_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.logisticscompany')),
            ],
            bases=('app.logisticscompany',),
        ),
        migrations.CreateModel(
            name='CarrierCompany',
            fields=[
                ('logisticscompany_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.logisticscompany')),
                ('is_main', models.BooleanField(default=False)),
            ],
            bases=('app.logisticscompany',),
        ),
        migrations.CreateModel(
            name='TrailerMake',
            fields=[
                ('unitmake_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.unitmake')),
            ],
            bases=('app.unitmake',),
        ),
        migrations.CreateModel(
            name='TruckMake',
            fields=[
                ('unitmake_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.unitmake')),
            ],
            bases=('app.unitmake',),
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=10, validators=[app.models.validators.validate_VIN])),
                ('trailer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='app.trailer')),
            ],
            bases=(models.Model, app.models.units.Unit),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=3)),
            ],
            options={
                'unique_together': {('name', 'code')},
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_coordinator', models.BooleanField(default=False)),
                ('roles', models.ManyToManyField(to='app.role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=app.models.files.get_file_path)),
                ('notes', models.CharField(blank=True, max_length=20, null=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=35)),
                ('middle_name', models.CharField(blank=True, max_length=35, null=True)),
                ('last_name', models.CharField(max_length=35)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('license_number', models.CharField(max_length=10, validators=[app.models.validators.validate_driver_license])),
                ('hire_type', models.CharField(choices=[('FR', 'Flat rate'), ('CPM', 'Cent per mile'), ('OWN', 'Owner')], max_length=3)),
                ('pay', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True, max_length=200, null=True)),
                ('coordinator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.profile', validators=[app.models.validators.validate_coordinator])),
                ('home_address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.address')),
                ('license_state', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.state')),
                ('truck', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='app.truck')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.carriercompany')),
            ],
            options={
                'unique_together': {('license_number', 'license_state')},
            },
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.state'),
        ),
        migrations.CreateModel(
            name='TruckModel',
            fields=[
                ('unitmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.unitmodel')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.truckmake')),
            ],
            bases=('app.unitmodel',),
        ),
        migrations.CreateModel(
            name='TruckGroup',
            fields=[
                ('unitgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.unitgroup')),
                ('trucks', models.ManyToManyField(to='app.truck')),
            ],
            bases=('app.unitgroup',),
        ),
        migrations.CreateModel(
            name='TruckFile',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.file')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.truck')),
            ],
            bases=('app.file',),
        ),
        migrations.AddField(
            model_name='truck',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.truckmodel'),
        ),
        migrations.CreateModel(
            name='TrailerModel',
            fields=[
                ('unitmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.unitmodel')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trailermake')),
            ],
            bases=('app.unitmodel',),
        ),
        migrations.CreateModel(
            name='TrailerGroup',
            fields=[
                ('unitgroup_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.unitgroup')),
                ('trailers', models.ManyToManyField(to='app.trailer')),
            ],
            bases=('app.unitgroup',),
        ),
        migrations.CreateModel(
            name='TrailerFile',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.file')),
                ('trailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.trailer')),
            ],
            bases=('app.file',),
        ),
        migrations.AddField(
            model_name='trailer',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.trailermodel'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.file')),
                ('issued_by', models.CharField(choices=[('DOT', 'Department of Transportation'), ('Police', 'Police')], default='DOT', max_length=6)),
                ('charged', models.BooleanField(default=False)),
                ('amt', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.driver')),
                ('issue_state', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.state')),
            ],
            bases=('app.file',),
        ),
        migrations.CreateModel(
            name='DriverFile',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.file')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.driver')),
            ],
            bases=('app.file',),
        ),
        migrations.AlterUniqueTogether(
            name='address',
            unique_together={('country', 'state', 'city', 'zip', 'street', 'building')},
        ),
    ]