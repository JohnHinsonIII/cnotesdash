from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin
from .models import Contracts, Attachments, Review, Document, LaborPosition, ClinReport, Employee


class ContractsResource(resources.ModelResource):
    class Meta:
        model = Contracts
        fields = ['id', 'user', 'contract_number', 'title', 'contract_status', 'contract_type', 'effective_date',
                  'expiration_date', 'renewal_date', 'total_funding', 'current_funding', 'funded',
                  'company_name', 'division', 'current_year']
        # the fields that we want to import


class AttachmentsResource(resources.ModelResource):
    class Meta:
        model = Attachments
        fields = ['contract_type', 'short_description', 'attach_file', 'contracts_id', 'created_date']
        # the fields that we want to import


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = ['text', 'created_date', 'user', 'contract', 'atRisk']
        # the fields that we want to import


class DocumentResource(resources.ModelResource):
    class Meta:
        model = Document
        fields = ['document_type', 'title', 'tag', 'created_date', 'user', 'contract', 'attach_file']
        # the fields that we want to import


class LaborPositionResource(resources.ModelResource):
    class Meta:
        model = LaborPosition
        fields = ['id', 'sins_proposed', 'job_title', 'educational_level', 'years_experience', 'price_year_1',
                  'price_year_2', 'price_year_3', 'price_year_4', 'price_year_5']
        # the fields that we want to import


class ClinReportResource(resources.ModelResource):
    class Meta:
        model = ClinReport
        fields = ['id', 'user', 'contracts', 'employees', 'item_number', 'supplies_services_description', 'qty', 'unit',
                  'unit_price',
                  'total_price', 'option_year', 'notes']
        # the fields that we want to import


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'contracts', 'last_name', 'first_name', 'middle_name']


@admin.register(Contracts)
class ContractsAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['contract_type', 'contract_status', 'tag_type', 'user', 'title', 'company_name', 'contract_number',
                    'created_date']
    search_fields = ['contract_status', 'contract_type', 'tag_type', 'contract_number']
    resource_class = ContractsResource


@admin.register(Attachments)
class AttachmentsAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['contract_type', 'contracts_id', 'short_description', 'attach_file', 'created_date']
    search_fields = ['contract_type', 'contracts_id', 'short_description', 'created_date']
    resource_class = AttachmentsResource


@admin.register(Review)
class ReviewAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['text', 'user', 'contract', 'atRisk']
    search_fields = ['text', 'user', 'contract', 'atRisk']
    resource_class = ReviewResource


@admin.register(Document)
class DocumentAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['document_type', 'title', 'tag', 'created_date', 'user', 'contract', 'attach_file']
    search_fields = ['document_type', 'title', 'tag', 'created_date', 'user', 'contract']
    resource_class = DocumentResource


@admin.register(LaborPosition)
class LaborPositionAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['sins_proposed', 'job_title', 'educational_level', 'years_experience', 'price_year_1',
                    'price_year_2', 'price_year_3', 'price_year_4', 'price_year_5', 'created_date']
    search_fields = ['sins_proposed', 'job_title', 'educational_level', 'years_experience', 'price_year_1',
                     'price_year_2', 'price_year_3', 'price_year_4', 'price_year_5', 'created_date']
    resource_class = LaborPositionResource


@admin.register(ClinReport)
class ClinReportAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ['user', 'contracts', 'employees', 'employees', 'item_number', 'supplies_services_description', 'qty', 'unit', 'unit_price',
                    'total_price', 'option_year', 'notes', 'created_date']
    search_fields = ['user', 'contracts', 'employees', 'item_number', 'supplies_services_description', 'qty', 'unit', 'unit_price',
                     'total_price', 'option_year', 'notes', 'created_date']
    resource_class = ClinReportResource


@admin.register(Employee)
class EmployeeAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('user', 'contracts', 'last_name', 'first_name', 'middle_name')
    search_fields = ['user', 'contracts', 'last_name', 'first_name', 'middle_name']
    resource_class = EmployeeResource
