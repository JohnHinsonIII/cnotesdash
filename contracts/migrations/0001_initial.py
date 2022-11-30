# Generated by Django 4.1.3 on 2022-11-26 14:46

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(choices=[('Firm Fixed Price', 'Firm Fixed Price'), ('Fixed Price Incentive', 'Fixed Price Incentive'), ('Time and Materials', 'Time And Materials'), ('Cost Plus Fixed Fee', 'Cost Plus Fixed Fee'), ('Cost Plus Incentive Fees', 'Cost Plus Incentive Fees'), ('Cost Plus Award Fee', 'Cost Plus Award Fee')], default='Firm Fixed Price', max_length=50)),
                ('contract_status', models.CharField(choices=[('Active', 'Active'), ('Awarded', 'Awarded'), ('Closed', 'Closed'), ('Draft', 'Draft'), ('In progress', 'In Progress'), ('New', 'New'), ('Not Awarded', 'Not Awarded'), ('Pending', 'Pending')], default='Active', max_length=50)),
                ('tag_type', models.CharField(choices=[('Cohorts', 'Cohorts'), ('Colleges', 'Colleges'), ('Education', 'Education'), ('Government', 'Government'), ('IT', 'It'), ('Non Profits', 'Non Profits'), ('Private Consumer', 'Private Clint'), ('Public Health', 'Public Health'), ('Universities', 'Universities'), ('Other', 'Other')], default='Government', max_length=50)),
                ('title', models.CharField(default='IHRC -', max_length=100)),
                ('company_name', models.CharField(default='IHRC INC.', max_length=100)),
                ('contract_number', models.CharField(default='000-000-0000-YYYY', max_length=100)),
                ('office', models.CharField(blank=True, default='Atlanta', max_length=100, null=True)),
                ('division', models.CharField(blank=True, default='CORPORATE ', max_length=100, null=True)),
                ('short_description', ckeditor.fields.RichTextField(blank=True, default='The short description is  ', null=True)),
                ('effective_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('renewal_date', models.DateField(blank=True, null=True)),
                ('prime', models.CharField(blank=True, max_length=100, null=True)),
                ('prime_pm', models.CharField(blank=True, max_length=100, null=True)),
                ('sub', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_pm', models.CharField(blank=True, max_length=100, null=True)),
                ('current_year', models.CharField(blank=True, default='Option Year 1 ', max_length=100, null=True)),
                ('total_funding', models.FloatField(blank=True, null=True)),
                ('current_funding', models.FloatField(blank=True, null=True)),
                ('funded', models.FloatField(blank=True, null=True)),
                ('city', models.CharField(blank=True, default='Atlanta', max_length=100)),
                ('state', models.CharField(blank=True, default='Georgia', max_length=100)),
                ('zipcode', models.CharField(blank=True, default='30082', max_length=100)),
                ('contact_email', models.CharField(blank=True, default='first_name@ihrc.com', max_length=50)),
                ('contract_award', models.FileField(blank=True, null=True, upload_to='contract-docs/')),
                ('contract_amendment', models.FileField(blank=True, null=True, upload_to='contract-docs/')),
                ('contract_renewal', models.FileField(blank=True, null=True, upload_to='contract-docs/')),
                ('contract_nda', models.FileField(blank=True, null=True, upload_to='contract-docs/')),
                ('main_logo', models.ImageField(blank=True, null=True, upload_to='')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_time', models.DateTimeField(db_index=True, default=datetime.datetime(2022, 11, 26, 9, 46, 55, 355225))),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contract',
                'verbose_name_plural': 'Contracts',
            },
        ),
        migrations.CreateModel(
            name='LaborPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sins_proposed', models.CharField(blank=True, max_length=100, null=True)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('educational_level', models.CharField(blank=True, max_length=100, null=True)),
                ('years_experience', models.IntegerField(blank=True, null=True)),
                ('price_year_1', models.FloatField(blank=True, null=True)),
                ('price_year_2', models.FloatField(blank=True, null=True)),
                ('price_year_3', models.FloatField(blank=True, null=True)),
                ('price_year_4', models.FloatField(blank=True, null=True)),
                ('price_year_5', models.FloatField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_time', models.DateTimeField(db_index=True, default=datetime.datetime(2022, 11, 26, 9, 46, 55, 357218))),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'LaborPosition',
                'verbose_name_plural': 'LaborPositions',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('atRisk', models.BooleanField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=64, verbose_name='Last')),
                ('first_name', models.CharField(max_length=64, verbose_name='First')),
                ('middle_name', models.CharField(max_length=64, verbose_name='Middle')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_time', models.DateTimeField(db_index=True, default=datetime.datetime(2022, 11, 26, 9, 46, 55, 357218))),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('contracts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('Amendment', 'Amendment'), ('Award', 'Award'), ('Contractor Performance Assessment Reporting System', 'Cpars'), ('Deliverables', 'Deliverables'), ('Draft', 'Draft'), ('Modifications', 'Mods'), ('Non Disclosure Agreement', 'Nda'), ('New', 'New'), ('Progress Report', 'Progressreport'), ('Renewal', 'Renewal'), ('Sub-Contract Agreement', 'Subcontract')], default='Draft', max_length=50)),
                ('title', models.CharField(max_length=100)),
                ('tag', models.CharField(choices=[('Cohorts', 'Cohorts'), ('Colleges', 'Colleges'), ('Education', 'Education'), ('Government', 'Government'), ('IT', 'It'), ('Non Profits', 'Non Profits'), ('Private Consumer', 'Private Clint'), ('Public Health', 'Public Health'), ('Universities', 'Universities'), ('Other', 'Other')], default='Government', max_length=50)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('attach_file', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='ClinReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_number', models.CharField(blank=True, max_length=10, null=True)),
                ('supplies_services_description', models.CharField(blank=True, max_length=100, null=True)),
                ('qty', models.IntegerField(blank=True, null=True)),
                ('unit', models.CharField(choices=[('Ea', 'Each'), ('Lot', 'Lot'), ('Job', 'Job'), ('Other', 'Other')], default='Ea', max_length=10)),
                ('unit_price', models.IntegerField(blank=True, null=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('option_year', models.CharField(choices=[('0', 'Base Period'), ('1', 'Year 1'), ('2', 'Year 2'), ('3', 'Year 3'), ('4', 'Year 4'), ('5', 'Year 5'), ('6', 'Year 6'), ('7', 'Year 7'), ('8', 'Year 8'), ('9', 'Year 9'), ('10', 'Year 10')], default='0', max_length=10)),
                ('notes', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_time', models.DateTimeField(db_index=True, default=datetime.datetime(2022, 11, 26, 9, 46, 55, 358230))),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('contracts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts')),
                ('employees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.employee')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ClinReport',
                'verbose_name_plural': 'ClinReports',
            },
        ),
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(choices=[('Amendment', 'Amendment'), ('Award', 'Award'), ('Contractor Performance Assessment Reporting System', 'Cpars'), ('Deliverables', 'Deliverables'), ('Draft', 'Draft'), ('Modifications', 'Mods'), ('Non Disclosure Agreement', 'Nda'), ('New', 'New'), ('Progress Report', 'Progressreport'), ('Renewal', 'Renewal'), ('Sub-Contract Agreement', 'Subcontract')], default='Award', max_length=50)),
                ('short_description', models.CharField(blank=True, max_length=255, null=True)),
                ('attach_file', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_time', models.DateTimeField(db_index=True, default=datetime.datetime(2022, 11, 26, 9, 46, 55, 356235))),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('contracts_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contracts')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
    ]
