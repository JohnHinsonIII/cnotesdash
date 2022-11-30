from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views import View

from contracts.forms import ContractForm, ReviewForm, DocumentForm, ContactForm, AttachmentForm
from .filters import ContractFilter
from .models import Contracts, Attachments, Review, Document
from contracts.common.utils.process import html_to_pdf
from django.core.mail import BadHeaderError, send_mail


# Create your views here.
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('contracts/index.html')
    user_name = request.user.username
    # my_index_contracts = Contracts.objects.order_by('-created_date')
    # if user_name == "admin" or user_name == "contractsadmin":
    #    my_index_contracts = Contracts.objects.order_by('-created_date')
    # else:
    # my_index_contracts = request.user.objects.order_by('-created_date')
    my_index_contracts = Contracts.objects.order_by('-created_date')

    context = {"my_index_contracts": my_index_contracts}
    context.update(dict(Contracts.total_info()))
    context['best_month'] = Contracts.best_month()
    context['contracts_month_report'], context['contracts_month_report_labels'] = Contracts.contracts_month_report()

    return HttpResponse(html_template.render(context, request))
    #  return render(request, html_template)


def all_contracts(request):
    all_contracts = Contracts.objects.order_by('-created_date')
    my_Filter = ContractFilter(request.GET, queryset=all_contracts)
    all_contracts = my_Filter.qs

    context = {"all_contracts": all_contracts, "my_Filter": my_Filter}
    return render(request, 'contracts/all_contracts.html', context)


def new_contract(request):
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
            return redirect('contracts:all_contracts')

    context = {"form": form}
    return render(request, 'contracts/new_contract.html', context)


def detail(request, detail_id):
    detail = Contracts.objects.get(id=detail_id)

    attach = Attachments.objects.filter(contracts_id=detail)

    reviews = Review.objects.filter(contract=detail)

    documents = Document.objects.filter(contract=detail)

    context = {'detail': detail, 'attachments': attach, 'reviews': reviews, 'documents': documents}

    return render(request, 'contracts/detail.html', context)


def my_contracts(request):
    user_name = request.user.username

    if user_name == "admin" or user_name == "contractsadmin":
        my_contracts = Contracts.objects.order_by('-created_date')
    else:
        my_contracts = request.user.contracts_set.order_by('-created_date')

    print('user logged in: ' + user_name)
    context = {"my_contracts": my_contracts}
    return render(request, 'contracts/my_contracts.html', context)


def edit_contract(request, edit_id):
    contract = Contracts.objects.get(id=edit_id)

    if request.method != 'POST':
        form = ContractForm(instance=contract)
    else:
        form = ContractForm(request.POST, request.FILES, instance=contract)

        if form.is_valid():
            form.save()
            return redirect('contracts:my_contracts')

    context = {"contract": contract, 'form': form}
    return render(request, 'contracts/edit_contract.html', context)


def delete_contract(request, delete_id):
    contract = Contracts.objects.get(id=delete_id)

    if request.method == 'POST':
        contract.delete()
        return redirect('contracts:my_contracts')

    context = {"contract": contract}
    return render(request, 'contracts/delete_contract.html', context)


def create_review(request, contract_id):
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

            return redirect('contracts:detail', newReview.contract.id)

    context = {"form": form, 'contract': contract}
    return render(request, 'contracts/new_review.html', context)


def update_review(request, review_id):
    # review = Review.objects.get(id=review_id)
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    if request.method != 'POST':
        form = ReviewForm(instance=review)
    else:
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('contracts:detail', review.contract.id)

    context = {"review": review, 'form': form}
    return render(request, 'contracts/update_review.html', context)


def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)

    review.delete()

    return redirect('contracts:detail', review.contract.id)


def create_document(request, contract_id):
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

            return redirect('contracts:detail', newDocument.contract.id)

    context = {"form": form, 'contract': contract}
    return render(request, 'contracts/new_document.html', context)


def update_document(request, document_id):
    # review = Review.objects.get(id=review_id)
    document = get_object_or_404(Document, pk=document_id, user=request.user)

    if request.method != 'POST':
        form = DocumentForm(instance=document)
    else:
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('contracts:detail', document.contract.id)

    context = {"document": document, 'form': form}
    return render(request, 'contracts/update_document.html', context)


def delete_document(request, document_id):
    document = get_object_or_404(Review, pk=document_id, user=request.user)

    document.delete()

    return redirect('contracts:detail', document.contract.id)


# Creating a class based view
class GeneratePdf(View):
    def get(self, request, detail_id, *args, **kwargs):
        # report_data = Contracts.objects.all()
        report_data = Contracts.objects.get(id=detail_id)

        context = {"report_data": report_data}
        # invoice
        pdf = html_to_pdf('pdf/invoice-details.html', context)
        # getting the template
        # pdf = html_to_pdf('pdf/results.html', context)
        # All Reports
        # pdf = html_to_pdf('pdf/results-all.html', context)

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')


def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            name = form.cleaned_data['name']
            company = form.cleaned_data['company']
            phone = form.cleaned_data['phone']
            try:
                send_mail(subject, message, from_email, ['johnhhinsoniii@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "pdf/email.html", {'form': form})


def thanks(request):
    return HttpResponse('Thank you for your message.')


def add_attachment(request):
    if request.method != 'POST':
        form = AttachmentForm()
    else:
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('contracts:add_attachment')
    att = Attachments.objects.all()
    context = {"form": form, "attachments": att}
    return render(request, 'contracts/attachments.html', context)


# edit and update function
def update_data(request, edit_id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm = AttachmentForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = User.objects.get(pk=id)
        fm = AttachmentForm(instance=pi)

    return render(request, 'contracts/attachments.html', {'form': fm})


# delete function
def delete_data(request, delete_id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('contracts/attachments.html')
