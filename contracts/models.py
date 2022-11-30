import datetime

from django.contrib.admin.models import LogEntryManager
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum, Count, Max
from django.template.defaultfilters import date
from django.utils.timezone import now
from ckeditor.fields import RichTextField

from core import settings


# Create your models here.


class Contracts(models.Model):
    DEFAULT_CONTRACT_NUMBER = "000-000-0000-YYYY"
    DEFAULT_CONTRACT_TITLE = "IHRC -"
    DEFAULT_COMPANY_NAME = "IHRC INC."
    DEFAULT_CITY = "Atlanta"
    DEFAULT_STATE = "Georgia"
    DEFAULT_ZIPCODE = "30082"
    DEFAULT_EMAIL = "first_name@ihrc.com"
    DEFAULT_DIVISION = "CORPORATE "
    DEFAULT_OFFICE = "CORPORATE "
    DEFAULT_CURRENT_YEAR = "Option Year 1 "
    DEFAULT_SHORT_DESC = "The short description is  "
    DEFAULT_SOW_DESC = "The Statement of Work description is "
    DEFAULT_TASK_DESC = "The Task Description is "

    MONTHS = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
              11: 'Nov', 12: 'Dec'}

    class ContractType(models.TextChoices):
        FIRM_FIXED_PRICE = "Firm Fixed Price"
        Fixed_PRICE_INCENTIVE = "Fixed Price Incentive"
        TIME_AND_MATERIALS = "Time and Materials"
        COST_PLUS_FIXED_FEE = "Cost Plus Fixed Fee"
        COST_PLUS_INCENTIVE_FEES = "Cost Plus Incentive Fees"
        COST_PLUS_AWARD_FEE = "Cost Plus Award Fee"

    class ContractStatus(models.TextChoices):
        ACTIVE = "Active"
        AWARDED = "Awarded"
        CLOSED = "Closed"
        DRAFT = "Draft"
        IN_PROGRESS = "In progress"
        NEW = "New"
        NOT_AWARDED = "Not Awarded"
        PENDING = "Pending"

    class TagType(models.TextChoices):
        COHORTS = "Cohorts"
        COLLEGES = "Colleges"
        EDUCATION = "Education"
        GOVERNMENT = "Government"
        IT = "IT"
        NON_PROFITS = "Non Profits"
        PRIVATE_CLINT = "Private Consumer"
        PUBLIC_HEALTH = "Public Health"
        UNIVERSITIES = "Universities"
        OTHER = "Other"

    contract_type = models.CharField(
        max_length=50,
        choices=ContractType.choices,
        default=ContractType.FIRM_FIXED_PRICE)

    contract_status = models.CharField(
        max_length=50,
        choices=ContractStatus.choices,
        default=ContractStatus.ACTIVE)

    tag_type = models.CharField(
        max_length=50,
        choices=TagType.choices,
        default=TagType.GOVERNMENT)

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default=DEFAULT_CONTRACT_TITLE)
    company_name = models.CharField(max_length=100, default=DEFAULT_COMPANY_NAME)
    contract_number = models.CharField(max_length=100, default=DEFAULT_CONTRACT_NUMBER)
    office = models.CharField(max_length=100, null=True, blank=True, default=DEFAULT_CITY)
    division = models.CharField(max_length=100, null=True, blank=True, default=DEFAULT_DIVISION)
    short_description = RichTextField(null=True, blank=True, default=DEFAULT_SHORT_DESC)
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    prime = models.CharField(max_length=100, null=True, blank=True)
    prime_pm = models.CharField(max_length=100, null=True, blank=True)
    sub = models.CharField(max_length=100, null=True, blank=True)
    sub_pm = models.CharField(max_length=100, null=True, blank=True)
    current_year = models.CharField(max_length=100, null=True, blank=True, default=DEFAULT_CURRENT_YEAR)
    total_funding = models.FloatField(null=True, blank=True)
    current_funding = models.FloatField(null=True, blank=True)
    funded = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True, default=DEFAULT_CITY)
    state = models.CharField(max_length=100, blank=True, default=DEFAULT_STATE)
    zipcode = models.CharField(max_length=100, blank=True, default=DEFAULT_ZIPCODE)
    contact_email = models.CharField(max_length=50, blank=True, default=DEFAULT_EMAIL)
    # contract_award = models.FileField(upload_to='contract-docs/', null=True, blank=True)
    # contract_amendment = models.FileField(upload_to='contract-docs/', null=True, blank=True)
    # contract_renewal = models.FileField(upload_to='contract-docs/', null=True, blank=True)
    # contract_nda = models.FileField(upload_to='contract-docs/', null=True, blank=True)
    main_logo = models.ImageField(null=True, blank=True)
    created_date = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    # start_time = models.TimeField()
    # end_time = models.TimeField()
    #
    # @classmethod
    # def duration(cls):
    #     return self.end_time - self.start_time

    @classmethod
    def total_info(cls):
        return cls.objects.aggregate(total_sales=Sum('funded'), total_contracts=Count('id'), peek_sale=Max('funded'))

    @classmethod
    def best_month(cls):
        res = {}
        month_funded = cls.objects.values_list('created_time__month').annotate(total=Sum('funded'))
        if month_funded:
            res['month'], res['funded'] = max(month_funded, key=lambda i: i[1])
            res['month_name'] = date(datetime.date(datetime.datetime.now().year, month=res['month'], day=1), 'F')
        return res

    @classmethod
    def contracts_month_report(cls):
        now = datetime.datetime.now()

        month_val = now.month + 1

        # Limit the upper value
        if month_val > 12:
            month_val = 12

        filter_params = {
            'created_time__date__gte': '{year}-{month}-{day}'.format(year=now.year - 1, month=month_val,
                                                                     day=now.day),
            'created_time__date__lte': now.date()
        }

        annotate_params = {
            'total_contract': Count('id'),
            'total_funded': Sum('funded')
        }

        queryset = cls.objects.filter(**filter_params).values('created_time__year', 'created_time__month').annotate(
            **annotate_params)

        return list(queryset), [cls.MONTHS[data.get('created_time__month')] for data in queryset]


class Attachments(models.Model):
    class FileType(models.TextChoices):
        AMENDMENT = "Amendment"
        AWARD = "Award"
        CPARS = "Contractor Performance Assessment Reporting System"
        DELIVERABLES = "Deliverables"
        DRAFT = "Draft"
        MODS = "Modifications"
        NDA = "Non Disclosure Agreement"
        NEW = "New"
        PROGRESSREPORT = "Progress Report"
        RENEWAL = "Renewal"
        SUBCONTRACT = "Sub-Contract Agreement"

    contract_type = models.CharField(
        max_length=50,
        choices=FileType.choices,
        default=FileType.AWARD)
    short_description = models.CharField(max_length=255, null=True, blank=True)
    attach_file = models.FileField(upload_to='attachments/', null=True, blank=True)
    contracts_id = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_description

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"


class Review(models.Model):
    # text = models.CharField(max_length=100)
    text = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    atRisk = models.BooleanField()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"


class Document(models.Model):
    class DocumentType(models.TextChoices):
        AMENDMENT = "Amendment"
        AWARD = "Award"
        CPARS = "Contractor Performance Assessment Reporting System"
        DELIVERABLES = "Deliverables"
        DRAFT = "Draft"
        MODS = "Modifications"
        NDA = "Non Disclosure Agreement"
        NEW = "New"
        PROGRESSREPORT = "Progress Report"
        RENEWAL = "Renewal"
        SUBCONTRACT = "Sub-Contract Agreement"

    class TagDocType(models.TextChoices):
        COHORTS = "Cohorts"
        COLLEGES = "Colleges"
        EDUCATION = "Education"
        GOVERNMENT = "Government"
        IT = "IT"
        NON_PROFITS = "Non Profits"
        PRIVATE_CLINT = "Private Consumer"
        PUBLIC_HEALTH = "Public Health"
        UNIVERSITIES = "Universities"
        OTHER = "Other"

    document_type = models.CharField(
        max_length=50,
        choices=DocumentType.choices,
        default=DocumentType.DRAFT)

    title = models.CharField(max_length=100)

    tag = models.CharField(
        max_length=50,
        choices=TagDocType.choices,
        default=TagDocType.GOVERNMENT)

    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    attach_file = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"


class LaborPosition(models.Model):
    sins_proposed = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)
    educational_level = models.CharField(max_length=100, null=True, blank=True)
    years_experience = models.IntegerField(null=True, blank=True)
    price_year_1 = models.FloatField(null=True, blank=True)
    price_year_2 = models.FloatField(null=True, blank=True)
    price_year_3 = models.FloatField(null=True, blank=True)
    price_year_4 = models.FloatField(null=True, blank=True)
    price_year_5 = models.FloatField(null=True, blank=True)
    created_date = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title

    class Meta:
        verbose_name = "LaborPosition"
        verbose_name_plural = "LaborPositions"


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contracts = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    last_name = models.CharField("Last", max_length=64)
    first_name = models.CharField("First", max_length=64)
    middle_name = models.CharField("Middle", max_length=64)
    created_date = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


class ClinReport(models.Model):
    class OptionYear(models.TextChoices):
        BASE_PERIOD = "0"
        YEAR_1 = "1"
        YEAR_2 = "2"
        YEAR_3 = "3"
        YEAR_4 = "4"
        YEAR_5 = "5"
        YEAR_6 = "6"
        YEAR_7 = "7"
        YEAR_8 = "8"
        YEAR_9 = "9"
        YEAR_10 = "10"

    class UnitType(models.TextChoices):
        EACH = "Ea"
        LOT = "Lot"
        JOB = "Job"
        OTHER = "Other"

    # ['user', 'contracts', 'item_number', 'supplies_services_description', 'unit', 'unit_price',
    # 'total_price', 'option_year', 'notes', 'created_date']
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contracts = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    employees = models.ForeignKey(Employee, on_delete=models.CASCADE)
    item_number = models.CharField(max_length=10, null=True, blank=True)
    supplies_services_description = models.CharField(max_length=100, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True)
    unit = models.CharField(
        max_length=10,
        choices=UnitType.choices,
        default=UnitType.EACH)
    unit_price = models.IntegerField(null=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)
    option_year = models.CharField(
        max_length=10,
        choices=OptionYear.choices,
        default=OptionYear.BASE_PERIOD)
    notes = RichTextField(null=True, blank=True)
    created_date = models.DateTimeField(default=now)
    created_time = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.supplies_services_description

    class Meta:
        verbose_name = "ClinReport"
        verbose_name_plural = "ClinReports"

