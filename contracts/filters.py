from dataclasses import fields
import django_filters
from .models import Contracts


class ContractFilter(django_filters.FilterSet):
    class Meta:
        model = Contracts
        fields = ['contract_status', 'contract_type', 'tag_type', 'contract_number']
