import self
from django import forms
from django.forms import ModelForm, Textarea
from django.http import request

from core import settings
from .models import Contracts, Attachments, Review, Document, LaborPosition, ClinReport, Employee


class DateInput(forms.DateInput):
    input_type = 'date'


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contracts

        fields = ['contract_type', 'contract_status', 'tag_type', 'title', 'company_name', 'contract_number',
                  'office', 'division', 'short_description', 'effective_date',
                  'expiration_date', 'renewal_date', 'prime', 'prime_pm', 'sub', 'sub_pm', 'current_year',
                  'total_funding', 'current_funding', 'funded', 'city', 'state', 'zipcode', 'contact_email',
                  'main_logo',
                  'created_date']

        widgets = {
            'short_description': Textarea(
                attrs={'class': 'form-control', 'rows': 80, 'cols': 20}),
            'effective_date': DateInput(),
            'expiration_date': DateInput(),
            'renewal_date': DateInput(),
            'created_date': forms.TextInput(
                attrs={'class': 'form-control', 'readonly': 'readonly'}
            )
        }


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachments

        fields = ['contract_type', 'contracts_id', 'short_description', 'attach_file']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review

        fields = ['text', 'atRisk']

        widgets = {
            'text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
            'atRisk': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'title': 'At Risk'}
            )
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document

        fields = ['document_type', 'title', 'tag', 'attach_file']


class LaborPositionForm(forms.ModelForm):
    class Meta:
        model = LaborPosition

        fields = ['sins_proposed', 'job_title', 'educational_level', 'years_experience', 'price_year_1',
                  'price_year_2', 'price_year_3', 'price_year_4', 'price_year_5']


class ClinReportForm(forms.ModelForm):
    class Meta:
        model = ClinReport

        fields = ['user', 'contracts', 'employees', 'item_number', 'supplies_services_description', 'qty', 'unit', 'unit_price',
                  'total_price', 'option_year', 'notes']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee

        fields = ['user', 'contracts', 'last_name', 'first_name', 'middle_name']


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=False, )
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 43, 'rows': 8}))
    name = forms.CharField(required=True)
    phone = forms.CharField(required=False)
    company = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['from_email'].widget.attrs['placeholder'] = 'Email'
        self.fields['subject'].widget.attrs['placeholder'] = 'Subject'
        self.fields['message'].widget.attrs['placeholder'] = 'Message'
        self.fields['name'].widget.attrs['placeholder'] = 'Name'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone'
        self.fields['company'].widget.attrs['placeholder'] = 'Company'
