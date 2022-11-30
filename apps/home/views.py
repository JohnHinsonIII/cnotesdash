# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.views import View

from contracts.common.utils.process import html_to_pdf
from contracts.filters import ContractFilter
from contracts.forms import ContractForm, DocumentForm, ReviewForm
from contracts.models import Contracts, Attachments, Review, Document
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)


@login_required(login_url="/login/")
def index(request):
    # Get page number from request,
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)

    home_index_contracts = Contracts.objects.order_by('-created_date')
    all_contracts = Contracts.objects.order_by('-created_date')
    items = Contracts.objects.all()

    # Paginate items
    items_per_page = 10
    paginator = Paginator(items, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    # Provide filtered, paginated library items
    context = {"items_page": items_page}

    context = {'segment': 'index'}
    context = {"all_contracts": all_contracts, "my_index_contracts": home_index_contracts, "items_page": items_page}
    context.update(dict(Contracts.total_info()))
    context['best_month'] = Contracts.best_month()
    context['contracts_month_report'], context['contracts_month_report_labels'] = Contracts.contracts_month_report()
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


def add_contract(request):
    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = ContractForm()
    else:
        # POST data submitted, process data.
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new entry and assign to contract.
            add_new_contract = form.save(commit=False)
            # Set the new contract attribute to the current user.
            add_new_contract.user = request.user
            # Save to database now the object has all the required data.
            add_new_contract.save()
            return redirect('all_contracts')

    context = {"form": form}
    # return render(request, 'contracts/add_contract.html', context)
    html_template = loader.get_template('home/add_contract.html')
    return HttpResponse(html_template.render(context, request))


def update_contract(request, edit_id):
    contract = Contracts.objects.get(id=edit_id)

    if request.method != 'POST':
        form = ContractForm(instance=contract)
    else:
        form = ContractForm(request.POST, request.FILES, instance=contract)

        if form.is_valid():
            form.save()
            return redirect('all_contracts')

    context = {"contract": contract, 'form': form}
    # return render(request, 'contracts/update_contract.html', context)
    html_template = loader.get_template('home/update_contract.html')
    return HttpResponse(html_template.render(context, request))


def detail_contracts(request, detail_id):
    detail_contract = Contracts.objects.get(id=detail_id)

    attach = Attachments.objects.filter(contracts_id=detail_contract)

    reviews = Review.objects.filter(contract=detail_contract)

    documents = Document.objects.filter(contract=detail_contract)

    context = {'detail_contract': detail_contract, 'attachments': attach, 'reviews': reviews, 'documents': documents}

    # return render(request, 'contracts/detail.html', context)
    html_template = loader.get_template('home/detail_contract.html')
    return HttpResponse(html_template.render(context, request))


def delete_contract(request, delete_id):
    contract = Contracts.objects.get(id=delete_id)

    if request.method == 'POST':
        contract.delete()
        return redirect('all_contracts')

    context = {"contract": contract}
    # return render(request, 'contracts/delete_contract.html', context)
    html_template = loader.get_template('home/delete_contract.html')
    return HttpResponse(html_template.render(context, request))


def add_review(request, contract_id):
    contract = get_object_or_404(Contracts, pk=contract_id)

    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = ReviewForm()
    else:
        # POST data submitted, process data.
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new entry and assign to contract.
            newReview = form.save(commit=False)
            # Set the new contract attribute to the current user.
            newReview.user = request.user
            # Save to database now the object has all the required data.
            newReview.contract = contract

            newReview.save()

            return redirect('detail_contracts', newReview.contract.id)

    context = {"form": form, 'contract': contract}
    # return render(request, 'contracts/new_review.html', context)
    html_template = loader.get_template('home/add_review.html')
    return HttpResponse(html_template.render(context, request))


def update_review(request, review_id):
    # review = Review.objects.get(id=review_id)
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method != 'POST':
        form = ReviewForm(instance=review)
    else:
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('detail_contracts', review.contract.id)

    context = {"review": review, 'form': form}
    # return render(request, 'contracts/update_review.html', context)
    html_template = loader.get_template('home/update_review.html')
    return HttpResponse(html_template.render(context, request))


def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    review.delete()

    return redirect('detail_contracts', review.contract.id)


def add_document(request, contract_id):
    contract = get_object_or_404(Contracts, pk=contract_id)

    if request.method != 'POST':
        # No data submitted, create a blank form.
        form = DocumentForm()
    else:
        # POST data submitted, process data.
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new entry and assign to contract.
            newDocument = form.save(commit=False)
            # Set the new contract attribute to the current user.
            newDocument.user = request.user
            # Save to database now the object has all the required data.
            newDocument.contract = contract

            newDocument.save()

            return redirect('detail_contracts', newDocument.contract.id)

    context = {"form": form, 'contract': contract}
    # return render(request, 'contracts/new_document.html', context)
    html_template = loader.get_template('home/add_document.html')
    return HttpResponse(html_template.render(context, request))


def update_document(request, document_id):
    # review = Review.objects.get(id=review_id)
    document = get_object_or_404(Document, pk=document_id, user=request.user)

    if request.method != 'POST':
        form = DocumentForm(instance=document)
    else:
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('detail_contracts', document.contract.id)

    context = {"document": document, 'form': form}
    # return render(request, 'contracts/update_document.html', context)
    html_template = loader.get_template('home/update_document.html')
    return HttpResponse(html_template.render(context, request))


def delete_document(request, document_id):
    document = get_object_or_404(Review, pk=document_id, user=request.user)

    document.delete()

    return redirect('detail_contracts', document.contract.id)


def all_contracts(request):
    # Get page number from request,
    # default to first page
    default_page = 1
    page = request.GET.get('page', default_page)

    all_contracts = Contracts.objects.order_by('-created_date')
    items = Contracts.objects.all()

    my_Filter = ContractFilter(request.GET, queryset=all_contracts)
    all_contracts = my_Filter.qs

    # Paginate items
    items_per_page = 10
    paginator = Paginator(items, items_per_page)

    try:
        items_page = paginator.page(page)
    except PageNotAnInteger:
        items_page = paginator.page(default_page)
    except EmptyPage:
        items_page = paginator.page(paginator.num_pages)

    # Provide filtered, paginated library items
    context = {"items_page": items_page}
    context = {"all_contracts": all_contracts, "my_Filter": my_Filter, "items_page": items_page}
    # context = {"all_contracts": all_contracts, "items_page": items_page}
    # return render(request, 'contracts/all_contracts.html', context)

    html_template = loader.get_template('home/all_contracts.html')
    return HttpResponse(html_template.render(context, request))


class GeneratePdf(View):
    def get(self, request, detail_id, *args, **kwargs):
        # report_data = Contracts.objects.all()
        report_data = Contracts.objects.get(id=detail_id)

        context = {"report_data": report_data}
        # invoice
        pdf = html_to_pdf('home/pdf/results.html', context)
        # getting the template
        # pdf = html_to_pdf('pdf/results.html', context)
        # All Reports
        # pdf = html_to_pdf('pdf/results-all.html', context)

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
