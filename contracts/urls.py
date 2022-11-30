from django.contrib import admin
from django.urls import path
from . import views
from .views import GeneratePdf

app_name = 'contracts'

urlpatterns = [
    path('', views.index, name='index'),
    path('all_contracts/', views.all_contracts, name='all_contracts'),
    path('new_contract/', views.new_contract, name='new_contract'),
    path('all_contracts/<detail_id>/', views.detail, name='detail'),
    path('my_contracts/', views.my_contracts, name='my_contracts'),
    path('edit_contract/<edit_id>/', views.edit_contract, name='edit_contract'),
    path('delete_contract/<delete_id>/', views.delete_contract, name="delete_contract"),
    path('create_review/<int:contract_id>/', views.create_review, name='create_review'),
    path('update_review/<int:review_id>/', views.update_review, name='update_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('create_document/<int:contract_id>/', views.create_document, name='create_document'),
    path('update_document/<int:document_id>/', views.update_document, name='update_document'),
    path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
    path('pdf/<detail_id>/', GeneratePdf.as_view(), name='pdf'),
    path('email/', views.email,  name='email'),
    path('add_attachment/', views.add_attachment, name='add_attachment')
]